import threading
import time

from utils.exit import ExitHandler
from utils.joystick.joystick import JoystickManager, JoystickManagerCallback, Joystick
from utils.logging_utils import Logger
from robot.control.definitions import TWIPR_Control_Mode
from robot.twipr import TWIPR
from robot.settings import readSettings

logger = Logger("JoystickControl")
logger.setLevel('INFO')


# ======================================================================================================================
class StandaloneJoystickControl:
    joystick_manager: JoystickManager
    joystick: Joystick
    twipr: TWIPR

    robot_settings: dict
    _exit: bool = False
    _thread: threading.Thread

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, twipr: TWIPR):
        self.twipr = twipr
        self.joystick_manager = JoystickManager()

        self.joystick_manager.registerCallback(JoystickManagerCallback.JOYSTICK_MANAGER_CALLBACK_NEW_JOYSTICK,
                                               self._newJoystick_callback)
        self.joystick_manager.registerCallback(JoystickManagerCallback.JOYSTICK_MANAGER_CALLBACK_JOYSTICK_DISCONNECTED,
                                               self._joystickDisconnected_callback)


        self.robot_settings = readSettings()

        self.joystick = None
        self.exit = ExitHandler()
        self.exit.register(self.close)
        self._thread = threading.Thread(target=self._task, daemon=True)

    # ------------------------------------------------------------------------------------------------------------------
    def init(self):
        self.joystick_manager.init()

    # ------------------------------------------------------------------------------------------------------------------
    def start(self):
        self.joystick_manager.start()
        self._thread.start()

    # ------------------------------------------------------------------------------------------------------------------
    def close(self, *args, **kwargs):
        self._exit = True
        if self._thread.is_alive():
            self._thread.join()

    # ------------------------------------------------------------------------------------------------------------------
    def _task(self):
        while not self._exit:
            self._updateInputs()
            time.sleep(0.01)

    # ------------------------------------------------------------------------------------------------------------------
    def _updateInputs(self):
        if self.joystick is None:
            return
        # Read the controller inputs
        axis_forward = -self.joystick.axis[1]
        axis_turn = -self.joystick.axis[3]

        # Check the control mode
        if self.twipr.control.mode == TWIPR_Control_Mode.TWIPR_CONTROL_MODE_OFF:
            return

        if self.twipr.control.mode == TWIPR_Control_Mode.TWIPR_CONTROL_MODE_BALANCING:
            self.twipr.control.setNormalizedBalancingInput(axis_forward, axis_turn)

        elif self.twipr.control.mode == TWIPR_Control_Mode.TWIPR_CONTROL_MODE_VELOCITY:
            forward_cmd = axis_forward * self.robot_settings['external_inputs']['normalized_velocity_scale']['forward']
            turn_cmd = axis_turn * self.robot_settings['external_inputs']['normalized_velocity_scale']['turn']
            self.twipr.control.setSpeed(v=forward_cmd, psi_dot=turn_cmd)

    # ------------------------------------------------------------------------------------------------------------------
    def _newJoystick_callback(self, joystick, *args, **kwargs):
        if self.joystick is None:
            self.joystick = joystick

        self.joystick.setButtonCallback(button=0,
                                        event='down',
                                        function=self.twipr.control.setMode,
                                        parameters={'mode': TWIPR_Control_Mode.TWIPR_CONTROL_MODE_OFF})

        self.joystick.setButtonCallback(button=1,
                                        event='down',
                                        function=self.twipr.control.setMode,
                                        parameters={'mode': TWIPR_Control_Mode.TWIPR_CONTROL_MODE_BALANCING})

        self.joystick.setButtonCallback(button=2,
                                        event='down',
                                        function=self.twipr.control.setMode,
                                        parameters={'mode': TWIPR_Control_Mode.TWIPR_CONTROL_MODE_VELOCITY})

        logger.info("Joystick connected and assigned")

    # ------------------------------------------------------------------------------------------------------------------
    def _joystickDisconnected_callback(self, joystick, *args, **kwargs):
        if joystick == self.joystick:
            self.joystick = None

        self.twipr.control.setMode(TWIPR_Control_Mode.TWIPR_CONTROL_MODE_OFF)
        logger.info("Joystick disconnected")

    # ------------------------------------------------------------------------------------------------------------------
