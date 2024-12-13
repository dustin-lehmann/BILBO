import dataclasses
import threading
import time

from control_board.control_board import RobotControl_Board
from control_board.stm32.stm32 import resetSTM32
from utils.exit import ExitHandler
from utils.singletonlock.singletonlock import SingletonLock, terminate
from robot.communication.twipr_communication import TWIPR_Communication
from robot.control.definitions import TWIPR_Control_Mode
from robot.control.twipr_control import TWIPR_Control
from robot.drive.twipr_drive import TWIPR_Drive
from robot.estimation.twipr_estimation import TWIPR_Estimation
from robot.logging.twipr_logging import TWIPR_Logging
from robot.logging.twipr_sample import TWIPR_Sample_General
from robot.sensors.twipr_sensors import TWIPR_Sensors
from robot.settings import readSettings
from utils.logging_utils import Logger
from utils import IntervalTimer
from robot.supervisor.twipr_supervisor import TWIPR_Supervisor
from utils.revisions import get_versions, is_ll_version_compatible
from robot.utils.buzzer import beep

logger = Logger("TWIPR")


@dataclasses.dataclass
class TWIPR_Config:
    enable_wifi: bool = True
    enable_external_control: bool = True
    enable_external_startup: bool = True
    terminate_other_instances: bool = True


class TWIPR:

    config: TWIPR_Config

    board: RobotControl_Board

    communication: TWIPR_Communication
    control: TWIPR_Control
    estimation: TWIPR_Estimation
    drive: TWIPR_Drive
    sensors: TWIPR_Sensors

    supervisor: TWIPR_Supervisor
    lock: SingletonLock
    exit: ExitHandler
    _thread: threading.Thread
    _updateTimer: IntervalTimer = IntervalTimer(0.1)

    def __init__(self, config: TWIPR_Config = TWIPR_Config(), reset_stm32: bool = False):
        terminate(lock_file="/tmp/twipr.lock")
        self.lock = SingletonLock(lock_file="/tmp/twipr.lock", timeout=10)
        self.lock.__enter__()

        if reset_stm32:
            logger.info(f"Reset STM32. This takes ~2 Seconds")
            resetSTM32()
            time.sleep(3)

        # Load the settings from the settings file
        self.robot_settings = readSettings()

        # Set up the control board
        self.board = RobotControl_Board(device_class='robot', device_type='twipr', device_revision='v3',
                                        device_id=self.robot_settings['id'], device_name=self.robot_settings['name'])

        # Start the communication module (WI-FI, Serial and SPI)
        self.communication = TWIPR_Communication(board=self.board)

        # Set up the individual modules
        self.control = TWIPR_Control(comm=self.communication)
        self.estimation = TWIPR_Estimation(comm=self.communication)
        self.drive = TWIPR_Drive(comm=self.communication)
        self.sensors = TWIPR_Sensors(comm=self.communication)
        self.supervisor = TWIPR_Supervisor(comm=self.communication)
        self.logging = TWIPR_Logging(comm=self.communication,
                                     control=self.control,
                                     estimation=self.estimation,
                                     drive=self.drive,
                                     sensors=self.sensors,
                                     general_sample_collect_function=self._getSample)

        # Set up the thread in which the main module is running
        self._thread = threading.Thread(target=self._threadFunction)
        self.communication.wifi.addCommand(identifier='beep',
                                           callback=beep,
                                           arguments=['frequency', 'time_ms', 'repeats'],
                                           description='Beeps')
        self.exit = ExitHandler()
        self.exit.register(self._shutdown)

    # ==================================================================================================================
    def init(self):
        self.board.init()
        self.communication.init()
        self.control.init()
        self.supervisor.init()
        self.sensors.init()
        self.logging.init()

    # ------------------------------------------------------------------------------------------------------------------
    def start(self):
        self.board.start()
        self.communication.start()

        # Read the firmware revision
        if not self._checkFirmwareRevision():
            exit()

        success = self.control.start()

        if not success:
            logger.error("Cannot write control configuration. Exit program")
            exit()

        self.supervisor.start()
        self.sensors.start()
        self.logging.start()
        logger.info("Start TWIPR")
        self._thread.start()
        time.sleep(1)
        beep(frequency='middle')

    # ------------------------------------------------------------------------------------------------------------------
    def update(self):
        self.logging.update()

    # === PRIVATE FUNCTIONS ============================================================================================
    def _shutdown(self, *args, **kwargs):
        self.lock.__exit__(None, None, None)
        # Ensure that the control is turned off
        self.control.setMode(TWIPR_Control_Mode.TWIPR_CONTROL_MODE_OFF)
        # Beep for audio reference
        beep(frequency='low')
        exit(0)
        # time.sleep(1)

    # ------------------------------------------------------------------------------------------------------------------
    def _checkFirmwareRevision(self) -> bool:
        revision_stm32 = self.communication.serial.readFirmwareRevision()
        revision_data = get_versions()

        # Check if the LL firmware is compatible
        if revision_stm32 is None or not is_ll_version_compatible(current_ll_version=(revision_stm32['major'],
                                                                                      revision_stm32['minor']),
                                                                  min_ll_version=(
                                                                          revision_data['stm32_firmware']['major'],
                                                                          revision_data['stm32_firmware'][
                                                                              'minor'])):
            logger.error(
                f"STM32 Firmware not compatible. Current Version: {revision_stm32['major']}.{revision_stm32['minor']}."
                f" Required > {revision_data['stm32_firmware']['major']}.{revision_data['stm32_firmware']['minor']}")
            return False

        logger.info(
            f"Software Version {revision_data['software']['major']}.{revision_data['software']['minor']}"
            f" (STM32: {revision_stm32['major']}.{revision_stm32['minor']})")
        return True

    # ------------------------------------------------------------------------------------------------------------------
    def _getSample(self):
        sample = TWIPR_Sample_General()
        sample.status = 'ok'
        sample.id = self.robot_settings['id']
        sample.configuration = ''
        sample.time = self.communication.wifi.getTime()
        sample.tick = 0
        sample.sample_time = 0.1
        return sample

    # ------------------------------------------------------------------------------------------------------------------
    def _threadFunction(self):
        self._updateTimer.reset()
        while True:
            self.update()
            self._updateTimer.sleep_until_next()

    # ------------------------------------------------------------------------------------------------------------------
    def __del__(self):
        if hasattr(self, 'lock'):
            self.lock.__exit__(None, None, None)
