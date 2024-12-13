import copy
import threading

from utils.callbacks import Callback
from robot.communication.twipr_communication import TWIPR_Communication
import robot.settings as settings
import robot.definitions.stm32_addresses as addresses
from robot.definitions.stm32_control import *
from utils.logging_utils import Logger
from robot.control.definitions import *
from robot.control.settings import *
from utils.data import limit, are_lists_approximately_equal
from utils import IntervalTimer
from utils.delayed_executor import delayed_execution

logger = Logger('control')
logger.setLevel('INFO')


# =====================================================================================================================
class TWIPR_Control:
    _comm: TWIPR_Communication

    status: TWIPR_Control_Status
    mode: TWIPR_Control_Mode
    mode_ll: TWIPR_Control_Mode_LL
    status_ll: TWIPR_Control_Status_LL

    allow_external_input = True

    # input: TWIPR_Control_Input

    _thread: threading.Thread
    _updateTimer: IntervalTimer = IntervalTimer(0.1)

    # === INIT =========================================================================================================
    def __init__(self, comm: TWIPR_Communication):

        # Input Handling
        self._comm = comm

        # Load the settings from the settings file
        self.settings = settings.readSettings()

        # Prepare the properties
        self.status = TWIPR_Control_Status(TWIPR_Control_Status.TWIPR_CONTROL_STATE_ERROR)
        self.mode = TWIPR_Control_Mode(TWIPR_Control_Mode.TWIPR_CONTROL_MODE_OFF)
        self.status_ll = TWIPR_Control_Status_LL(TWIPR_Control_Status_LL.TWIPR_CONTROL_STATE_LL_ERROR)
        self.mode_ll = TWIPR_Control_Mode_LL(TWIPR_Control_Mode_LL.TWIPR_CONTROL_MODE_LL_OFF)

        self.input = TWIPR_ControlInput()

        # Register the STM32 Sample
        self._comm.registerCallback('rx_stm32_sample', self._onSTM32Sample)

        #
        self.callbacks = {
            # 'control_mode_change': [],

        }

        # Add Commands to the WIFI Module
        self._comm.wifi.addCommand(identifier='setControlMode',
                                   callback=self.setMode,
                                   arguments=['mode'],
                                   description='Sets the control mode')

        self._comm.wifi.addCommand(identifier='setNormalizedBalancingInput',
                                   callback=self.setNormalizedBalancingInput,
                                   arguments=['forward', 'turn'],
                                   description='Sets the Input')

        self._comm.wifi.addCommand(identifier='setSpeed',
                                   callback=self.setSpeed,
                                   arguments=['v', 'psi_dot'],
                                   description='Sets the Speed')

        self._thread = threading.Thread(target=self._threadFunction)

    # === METHODS ======================================================================================================
    def init(self):
        ...

    # ------------------------------------------------------------------------------------------------------------------
    def start(self):
        success = self._writeInitialControlConfiguration()
        if not success:
            return False

        self._thread.start()
        return True

    # ------------------------------------------------------------------------------------------------------------------
    def update(self):

        # Step 1:

        # TODO: This is a stupid idea
        if self.status_ll == TWIPR_Control_Status_LL.TWIPR_CONTROL_STATE_LL_ERROR:
            self.status = TWIPR_Control_Status.TWIPR_CONTROL_STATE_ERROR
        elif self.status_ll == TWIPR_Control_Status_LL.TWIPR_CONTROL_STATE_LL_NORMAL:
            self.status = TWIPR_Control_Status.TWIPR_CONTROL_STATE_NORMAL

        if self.mode_ll == TWIPR_Control_Mode_LL.TWIPR_CONTROL_MODE_LL_OFF:
            self.mode = TWIPR_Control_Mode.TWIPR_CONTROL_MODE_OFF
        elif self.mode_ll == TWIPR_Control_Mode_LL.TWIPR_CONTROL_MODE_LL_BALANCING:
            self.mode = TWIPR_Control_Mode.TWIPR_CONTROL_MODE_BALANCING
        elif self.mode_ll == TWIPR_Control_Mode_LL.TWIPR_CONTROL_MODE_LL_VELOCITY:
            self.mode = TWIPR_Control_Mode.TWIPR_CONTROL_MODE_VELOCITY

    # ------------------------------------------------------------------------------------------------------------------
    def registerCallback(self, callback_id, function: callable, parameters: dict = None, lambdas: dict = None,
                         **kwargs):
        callback = Callback(function, parameters, lambdas, **kwargs)

        if callback_id in self.callbacks:
            self.callbacks[callback_id].append(callback)
        else:
            raise Exception("Invalid Callback type")

    # ------------------------------------------------------------------------------------------------------------------
    def loadConfig(self, name):
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    def saveConfig(self, name, config=None):
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    def setMode(self, mode: (int, TWIPR_Control_Mode)):

        # Check if the mode exists
        if isinstance(mode, int):
            try:
                mode = TWIPR_Control_Mode(mode)
            except ValueError:
                logger.warning(f"Value of {mode} is not a valid control mode")
                return

        logger.info(f"Setting control mode to {mode.name}")

        # Depending on the mode, set the lower level control mode
        if mode == TWIPR_Control_Mode.TWIPR_CONTROL_MODE_OFF:
            self._setControlMode_LL(TWIPR_Control_Mode_LL.TWIPR_CONTROL_MODE_LL_OFF)
        elif mode == TWIPR_Control_Mode.TWIPR_CONTROL_MODE_BALANCING:
            self._setControlMode_LL(TWIPR_Control_Mode_LL.TWIPR_CONTROL_MODE_LL_BALANCING)
        elif mode == TWIPR_Control_Mode.TWIPR_CONTROL_MODE_VELOCITY:
            self._setControlMode_LL(TWIPR_Control_Mode_LL.TWIPR_CONTROL_MODE_LL_VELOCITY)

    # ------------------------------------------------------------------------------------------------------------------
    def standUp(self):
        if not self.mode == TWIPR_Control_Mode.TWIPR_CONTROL_MODE_OFF:
            return
        self.setMode(TWIPR_Control_Mode.TWIPR_CONTROL_MODE_BALANCING)
        delayed_execution(self.setMode, 1, mode=TWIPR_Control_Mode.TWIPR_CONTROL_MODE_VELOCITY)

    # ------------------------------------------------------------------------------------------------------------------
    def fallOver(self, direction='forward'):
        if not self.mode == TWIPR_Control_Mode.TWIPR_CONTROL_MODE_VELOCITY:
            return

        if direction == 'forward':
            self.setSpeed(v=0.2, psi_dot=0)
        elif direction == 'backward':
            self.setSpeed(v=-0.2, psi_dot=0)
        else:
            raise Exception("Invalid direction")

        delayed_execution(self.setMode, 0.5, mode=TWIPR_Control_Mode.TWIPR_CONTROL_MODE_OFF)

    def setNormalizedBalancingInput(self, forward: (int, float), turn: (int, float)):
        assert isinstance(forward, (int, float))
        assert isinstance(turn, (int, float))

        if self.mode_ll == TWIPR_Control_Mode_LL.TWIPR_CONTROL_MODE_LL_BALANCING:
            forward_cmd_scaled = forward * self.settings['external_inputs']['normalized_torque_scale']['forward']
            turn_cmd_scaled = turn * self.settings['external_inputs']['normalized_torque_scale']['turn']
            torque_left = -(forward_cmd_scaled + turn_cmd_scaled)
            torque_right = -(forward_cmd_scaled - turn_cmd_scaled)
            self.setBalancingInput(torque_left, torque_right)

    # ------------------------------------------------------------------------------------------------------------------
    def setBalancingInput(self, u_left: float, u_right: float):
        assert isinstance(u_left, float)
        assert isinstance(u_right, float)

        if self.mode_ll == TWIPR_Control_Mode_LL.TWIPR_CONTROL_MODE_LL_BALANCING:
            u_left = u_left + self.settings['control']['torque_offset'][0]
            u_right = u_right + self.settings['control']['torque_offset'][1]

            self._setBalancingInput_LL(u_left, u_right)

    # ------------------------------------------------------------------------------------------------------------------
    def setSpeed(self, v: float = 0, psi_dot: float = 0):
        assert isinstance(v, (int, float))
        assert isinstance(psi_dot, (int, float))

        if self.mode_ll == TWIPR_Control_Mode_LL.TWIPR_CONTROL_MODE_LL_VELOCITY:
            v = limit(v, TWIPR_CONTROL_VELOCITY_FORWARD_MAX)
            psi_dot = limit(psi_dot, TWIPR_CONTROL_VELOCITY_TURN_MAX)
            self._setSpeedInput_LL(v=v, psi_dot=psi_dot)

    # ------------------------------------------------------------------------------------------------------------------
    def setStateFeedbackGain(self, K):
        logger.info(f"Set State Feedback Gain to {K}")
        self._setStateFeedbackGain_LL(K)

    # ------------------------------------------------------------------------------------------------------------------
    def setVelocityControlPID_Forward(self, P: float, I: float, D: float):
        logger.info(f"Set Velocity Control PID Forward to {P}, {I}, {D}")
        self._setVelocityControlPIDForward_LL(P, I, D)

    # ------------------------------------------------------------------------------------------------------------------
    def setVelocityControlPID_Turn(self, P: float, I: float, D: float):
        logger.info(f"Set Velocity Control PID Turn to {P}, {I}, {D}")
        self._setVelocityControlPIDTurn_LL(P, I, D)

    # ------------------------------------------------------------------------------------------------------------------
    def setVelocityController(self, config: TWIPR_Speed_Control_Config):
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    def setMaxWheelSpeed(self, speed: (int, float)):
        assert (isinstance(speed, (int, float)))

        self._comm.serial.writeValue(module=addresses.TWIPR_AddressTables.REGISTER_TABLE_GENERAL,
                                     address=addresses.TWIPR_ControlAddresses.ADDRESS_CONTROL_RW_MAX_WHEEL_SPEED,
                                     value=float(speed),
                                     type=ctypes.c_float)

    # ------------------------------------------------------------------------------------------------------------------
    def getSample(self) -> TWIPR_Control_Sample:
        sample = TWIPR_Control_Sample()
        sample.status = self.status
        sample.mode = self.mode
        sample.configuration = ''
        sample.input = copy.copy(self.input)

        return sample

    # = PRIVATE METHODS ================================================================================================
    def _threadFunction(self):
        self._updateTimer.reset()
        while True:
            self.update()
            self._updateTimer.sleep_until_next()

    # ------------------------------------------------------------------------------------------------------------------
    def _onSTM32Sample(self, sample) -> None:
        self.status_ll = TWIPR_Control_Status_LL(sample['control']['status'])
        self.mode_ll = TWIPR_Control_Mode_LL(sample['control']['mode'])

        # self.input.input = 0  # TODO
        # self.input.input_ext = 0  # TODO
        # self.input.v_cmd = 0  # TODO
        # self.input.psi_dot_cmd = 0  # TODO

    # ------------------------------------------------------------------------------------------------------------------
    def _writeInitialControlConfiguration(self) -> bool:
        # Set State Feedback Gain
        self.setStateFeedbackGain(self.settings['control']['feedback_gain'])

        # Set PID Values
        self.setVelocityControlPID_Forward(P=self.settings['control']['pid_forward']['P'],
                                           I=self.settings['control']['pid_forward']['I'],
                                           D=self.settings['control']['pid_forward']['D'])

        self.setVelocityControlPID_Turn(P=self.settings['control']['pid_turn']['P'],
                                        I=self.settings['control']['pid_turn']['I'],
                                        D=self.settings['control']['pid_turn']['D'])

        # Read back the control config from the STM32
        config = self._readControlConfig_LL()
        # Check if the control has been set correctly
        if (config is None
            or not are_lists_approximately_equal(config['K'], self.settings['control']['feedback_gain'])
            or not are_lists_approximately_equal(
                    [self.settings['control']['pid_forward']['P'], self.settings['control']['pid_forward']['I'],
                     self.settings['control']['pid_forward']['D']],
                    [config['forward_p'], config['forward_i'], config['forward_d']])) \
                or not are_lists_approximately_equal(
            [self.settings['control']['pid_turn']['P'], self.settings['control']['pid_turn']['I'],
             self.settings['control']['pid_turn']['D']],
            [config['turn_p'], config['turn_i'], config['turn_d']]):
            logger.warning("Control Gains not set correctly")
            return False

        self.setMaxWheelSpeed(speed=self.settings['safety']['max_wheel_speed'])

        logger.info("Control Gains set correctly")
        return True

    # ------------------------------------------------------------------------------------------------------------------
    def _setControlMode_LL(self, mode: TWIPR_Control_Mode_LL) -> None:

        assert (isinstance(mode, TWIPR_Control_Mode_LL))

        self._comm.serial.executeFunction(module=addresses.TWIPR_AddressTables.REGISTER_TABLE_GENERAL,
                                          address=addresses.TWIPR_ControlAddresses.ADDRESS_CONTROL_SET_MODE,
                                          data=mode.value,
                                          input_type=ctypes.c_uint8)

    # ------------------------------------------------------------------------------------------------------------------
    def _readControlMode_LL(self):
        ...

    # ------------------------------------------------------------------------------------------------------------------
    def _readControlState_LL(self):
        ...

    # ------------------------------------------------------------------------------------------------------------------
    def _setStateFeedbackGain_LL(self, K) -> None:
        assert (isinstance(K, list))
        assert (len(K) == 8)
        assert (all(isinstance(elem, (float, int)) for elem in K))

        self._comm.serial.executeFunction(module=addresses.TWIPR_AddressTables.REGISTER_TABLE_GENERAL,
                                          address=addresses.TWIPR_ControlAddresses.ADDRESS_CONTROL_SET_K,
                                          data=K,
                                          input_type=ctypes.c_float * 8,
                                          output_type=None)

    # ------------------------------------------------------------------------------------------------------------------
    def _setVelocityControlPIDForward_LL(self, P: float, I: float, D: float) -> None:
        self._comm.serial.executeFunction(module=addresses.TWIPR_AddressTables.REGISTER_TABLE_GENERAL,
                                          address=addresses.TWIPR_ControlAddresses.ADDRESS_CONTROL_SET_FORWARD_PID,
                                          data=[P, I, D],
                                          input_type=ctypes.c_float * 3,
                                          output_type=None)

    # ------------------------------------------------------------------------------------------------------------------
    def _setVelocityControlPIDTurn_LL(self, P: float, I: float, D: float) -> None:
        self._comm.serial.executeFunction(module=addresses.TWIPR_AddressTables.REGISTER_TABLE_GENERAL,
                                          address=addresses.TWIPR_ControlAddresses.ADDRESS_CONTROL_SET_TURN_PID,
                                          data=[P, I, D],
                                          input_type=ctypes.c_float * 3,
                                          output_type=None)

    # ------------------------------------------------------------------------------------------------------------------
    def _setVelocityControl_LL(self):
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    def _setBalancingInput_LL(self, u_left: float, u_right: float):
        assert (isinstance(u_left, float))
        assert (isinstance(u_right, float))

        data = {
            'u_left': u_left,
            'u_right': u_right
        }

        self._comm.serial.executeFunction(module=addresses.TWIPR_AddressTables.REGISTER_TABLE_GENERAL,
                                          address=addresses.TWIPR_ControlAddresses.ADDRESS_CONTROL_SET_BALANCING_INPUT,
                                          data=data,
                                          input_type=twipr_control_balancing_input)

    # ------------------------------------------------------------------------------------------------------------------
    def _setSpeedInput_LL(self, v: float, psi_dot: float) -> None:
        assert (isinstance(v, (int, float)))
        assert (isinstance(psi_dot, (int, float)))

        data = {
            'forward': v,
            'turn': psi_dot
        }

        self._comm.serial.executeFunction(module=addresses.TWIPR_AddressTables.REGISTER_TABLE_GENERAL,
                                          address=addresses.TWIPR_ControlAddresses.ADDRESS_CONTROL_SET_SPEED_INPUT,
                                          data=data,
                                          input_type=twipr_control_speed_input)

    # ------------------------------------------------------------------------------------------------------------------
    def _setDirectInput_LL(self, u_left: float, u_right: float) -> None:
        assert (isinstance(u_left, float))
        assert (isinstance(u_right, float))
        data = {
            'u_left': u_left,
            'u_right': u_right
        }
        self._comm.serial.executeFunction(module=addresses.TWIPR_AddressTables.REGISTER_TABLE_GENERAL,
                                          address=addresses.TWIPR_ControlAddresses.ADDRESS_CONTROL_SET_DIRECT_INPUT,
                                          data=data,
                                          input_type=twipr_control_direct_input)

    # ------------------------------------------------------------------------------------------------------------------
    def _readControlConfig_LL(self) -> dict:
        return self._comm.serial.executeFunction(module=addresses.TWIPR_AddressTables.REGISTER_TABLE_GENERAL,
                                                 address=addresses.TWIPR_ControlAddresses.ADDRESS_CONTROL_READ_CONFIG,
                                                 data=None,
                                                 output_type=twipr_control_configuration_ll)

    # ------------------------------------------------------------------------------------------------------------------
