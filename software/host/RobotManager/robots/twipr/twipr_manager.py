from core.device_manager import DeviceManager
from core.device import Device
from utils.callbacks import Callback
from robots.twipr.twipr import TWIPR
from robots.twipr.twipr_definitions import TWIPR_ControlMode, TWIPR_IDS, TWIPR_PASSWORD, TWIPR_REMOTE_START_COMMAND, \
    TWIPR_USER_NAME, TWIPR_REMOTE_STOP_COMMAND
from robots.twipr.utils.twipr_scanner import TWIPR_Scanner
from utils.time import delayed_execution
from utils.exit import ExitHandler
from utils.logging import Logger
from utils.network.ssh import executeCommandOverSSH

logger = Logger('Robots')
logger.setLevel('INFO')


class TWIPR_Manager:
    """
    Manages the connection and control of TWIPR robots using the DeviceManager.
    Handles device events and provides methods to interact with connected robots.
    """

    deviceManager: DeviceManager
    callbacks: dict
    robots: dict[str, TWIPR]

    robot_auto_start: bool
    network_scanner: TWIPR_Scanner = None

    def __init__(self, robot_auto_start=True):
        """
        Initializes the TWIPR_Manager instance by setting up the device manager,
        registering callbacks, and initializing internal dictionaries for robots and callbacks.
        """
        self.deviceManager = DeviceManager()
        self.deviceManager.registerCallback('new_device', self._newDevice_callback)
        self.deviceManager.registerCallback('device_disconnected', self._deviceDisconnected_callback)
        self.deviceManager.registerCallback('stream', self._deviceStream_callback)

        self.robots = {}

        self.callbacks = {
            'new_robot': [],
            'robot_disconnected': [],
            'stream': []
        }

        self.scanner = None
        self.robot_auto_start = robot_auto_start
        if self.robot_auto_start:
            self.scanner = TWIPR_Scanner(TWIPR_IDS)

            self.scanner.registerCallback('robot_found', self._scannerRobotFound_callback)
            self.scanner.registerCallback('robot_lost', self._scannerRobotLost_callback)

        self.exit_handler = ExitHandler()
        self.exit_handler.register(self.close)

    @property
    def connected_robots(self):
        """
        Returns the number of connected robots.
        :return: Number of connected robots
        """
        return len(self.robots)

    # ------------------------------------------------------------------------------------------------------------------
    def registerCallback(self, callback_id, function, parameters: dict = None, lambdas: dict = None):
        """
        Registers a callback function for a specified callback ID.

        :param callback_id: ID of the callback to register
        :param function: Callback function to be executed
        :param parameters: Optional parameters for the callback
        :param lambdas: Optional lambda functions for the callback
        """
        callback = Callback(function, parameters, lambdas)
        if callback_id in self.callbacks:
            self.callbacks[callback_id].append(callback)
        else:
            raise Exception("Invalid Callback type")

    # ------------------------------------------------------------------------------------------------------------------
    def init(self):
        """
        Initializes the twipr manager.
        """
        self.deviceManager.init()

    # ------------------------------------------------------------------------------------------------------------------
    def start(self):
        """
        Starts the TWIPR Manager by initiating the device manager.
        """
        logger.info('Starting Twipr Manager')
        self.deviceManager.start()
        if self.scanner is not None:
            self.scanner.start()

    # ------------------------------------------------------------------------------------------------------------------
    def close(self, *args, **kwargs):
        logger.info("Close TWIPR Manager")
        if self.scanner is not None:
            active_robots = self.scanner.active_robots
            for name, address in active_robots.items():
                self._stopTWIPRRemote(name, address)

    # ------------------------------------------------------------------------------------------------------------------
    def getRobotById(self, robot_id):
        """
        Retrieves a robot instance by its ID.

        :param robot_id: ID of the robot to retrieve
        :return: TWIPR robot instance if found, None otherwise
        """
        if robot_id not in self.robots.keys():
            logger.warning(f"No robot with id {robot_id} is connected.")
            return None

        return self.robots[robot_id]

    # ------------------------------------------------------------------------------------------------------------------
    def emergencyStop(self):
        """
        Issues an emergency stop command to all connected robots.
        """
        logger.warning("Emergency Stop")
        for robot in self.robots.values():
            robot.setControlMode(TWIPR_ControlMode.TWIPR_CONTROL_MODE_OFF)

    # ------------------------------------------------------------------------------------------------------------------
    def setRobotControlMode(self, robot, mode):
        """
        Sets the control mode of a specified robot.

        :param robot: Robot instance or robot ID
        :param mode: Control mode to set (either as a string or an integer)
        """
        if isinstance(robot, str):
            if robot in self.robots.keys():
                robot = self.robots[robot]
            else:
                return

        if isinstance(mode, str):
            control_mode_dict = {"off": 0, "direct": 1, "balancing": 2, "speed": 3}
            if mode in control_mode_dict.keys():
                mode = control_mode_dict[mode]
            else:
                return

        robot.setControlMode(mode)

    # ------------------------------------------------------------------------------------------------------------------
    def _newDevice_callback(self, device: Device, *args, **kwargs):
        """
        Callback for handling new device connections.

        :param device: The newly connected device
        """
        # Check if the device has the correct class and type
        if not (device.information.device_class == 'robot' and device.information.device_type == 'twipr'):
            return
        robot = TWIPR(device)

        # Check if this robot ID is already used
        if robot.device.information.device_id in self.robots.keys():
            logger.warning(f"New Robot connected, but ID {robot.device.information.device_id} is already in use")

        self.robots[robot.device.information.device_id] = robot
        logger.info(f"New Robot connected with ID: \"{robot.device.information.device_id}\"")

        for callback in self.callbacks['new_robot']:
            callback(robot, *args, **kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    def _deviceDisconnected_callback(self, device, *args, **kwargs):
        """
        Callback for handling device disconnections.

        :param device: The disconnected device
        """
        if device.information.device_id not in self.robots:
            return

        robot = self.robots[device.information.device_id]
        self.robots.pop(device.information.device_id)

        logger.info(f"Robot {device.information.device_id} disconnected")

        # Remove any joystick assignments
        for callback in self.callbacks['robot_disconnected']:
            callback(robot, *args, **kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    def _deviceStream_callback(self, stream, device, *args, **kwargs):
        """
        Callback for handling data streams from devices.

        :param stream: The data stream
        :param device: The device sending the stream
        """
        if device.information.device_id in self.robots.keys():
            for callback in self.callbacks['stream']:
                callback(stream, self.robots[device.information.device_id], *args, **kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    def _scannerRobotFound_callback(self, name, ip_address, *args, **kwargs):
        logger.info(f"Scanner found robot {name} with IP address {ip_address}")
        self._startTWIPRRemote(name, ip_address)

    # ------------------------------------------------------------------------------------------------------------------
    def _scannerRobotLost_callback(self, name, ip_address, *args, **kwargs):
        logger.info(f"Scanner lost robot {name} with IP address {ip_address}")

    # ------------------------------------------------------------------------------------------------------------------
    def _startTWIPRRemote(self, name, ip_address, *args, **kwargs):
        logger.info(f"Starting {name} remotely via ssh")
        delayed_execution(executeCommandOverSSH, delay=0.25, hostname=ip_address,
                          username=TWIPR_USER_NAME,
                          password=TWIPR_PASSWORD,
                          command=TWIPR_REMOTE_STOP_COMMAND)

        delayed_execution(executeCommandOverSSH, delay=2, hostname=ip_address,
                          username=TWIPR_USER_NAME,
                          password=TWIPR_PASSWORD,
                          command=TWIPR_REMOTE_START_COMMAND)

    # ------------------------------------------------------------------------------------------------------------------
    def _stopTWIPRRemote(self, name, ip_address, *args, **kwargs):
        logger.info(f"Stopping {name} remotely via ssh")
        executeCommandOverSSH(hostname=ip_address,
                              username=TWIPR_USER_NAME,
                              password=TWIPR_PASSWORD,
                              command=TWIPR_REMOTE_STOP_COMMAND)
