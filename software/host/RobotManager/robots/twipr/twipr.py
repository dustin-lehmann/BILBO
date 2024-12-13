from core.device import Device
from robots.twipr.utils.twipr_data import TWIPR_Data, twiprSampleFromDict
from utils.logging import Logger

from robots.twipr.twipr_definitions import *

logger = Logger("TWIPR")
logger.setLevel("DEBUG")


class TWIPR:
    device: Device
    callbacks: dict
    data: TWIPR_Data

    def __init__(self, device: Device, *args, **kwargs):
        self.device = device

        self.callbacks = {
            'stream': []
        }

        self.data = TWIPR_Data()
        self.device.registerCallback('stream', self._onStreamCallback)

    # === CLASS METHODS =====================================================================

    # === METHODS ============================================================================

    # === PROPERTIES ============================================================================
    @property
    def id(self):
        return self.device.information.device_id

    # === COMMANDS ===========================================================================

    def balance(self, state):
        self.setControlMode(TWIPR_ControlMode.TWIPR_CONTROL_MODE_BALANCING)

    def setControlConfiguration(self, config):
        ...

    def loadControlConfiguration(self, name):
        ...

    def saveControlConfiguration(self, name):
        ...

    def beep(self, frequency, time_ms, repeats):
        self.device.command(command='beep', data={'frequency': 250, 'time_ms': 250, 'repeats': 1})

    def stop(self):
        self.setControlMode(0)

    def setControlMode(self, mode: TWIPR_ControlMode):
        logger.debug(f"Robot {self.id}: Set Control Mode to {mode}")
        self.device.command(command='setControlMode', data={'mode': mode})

    def setNormalizedBalancingInput(self, forward, turn, *args, **kwargs):
        self.device.command('setNormalizedBalancingInput', data={'forward': forward, 'turn': turn})

    def setSpeed(self, v, psi_dot, *args, **kwargs):
        self.device.command('setSpeed', data={'v': v, 'psi_dot': psi_dot})

    def setTorque(self, torque, *args, **kwargs):
        self.device.command('setControlInput', data={'input': torque})

    def setLEDs(self, color):
        ...

    def setTestParameter(self, value):
        ...

    def _onStreamCallback(self, stream, *args, **kwargs):
        self.data = twiprSampleFromDict(stream.data)

