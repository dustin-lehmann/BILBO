import time

from core.device import Device
from utils.callbacks import callback_handler, CallbackContainer


# ======================================================================================================================
@callback_handler
class Frodo_Callbacks:
    stream: CallbackContainer


# ======================================================================================================================
class Frodo:
    device: Device
    callbacks: Frodo_Callbacks

    def __init__(self, device: Device):
        self.device = device
        self.device.callbacks.stream.register(self._onStream_callback)
        self.callbacks = Frodo_Callbacks()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def id(self):
        return self.device.information.device_id

    # ------------------------------------------------------------------------------------------------------------------
    def setSpeed(self, speed_left, speed_right):
        self.device.function(function='setSpeed',
                             data={
                                 'speed_left': speed_left,
                                 'speed_right': speed_right
                             })

    # ------------------------------------------------------------------------------------------------------------------
    def beep(self):
        self.device.function(function='beep', data={'frequency': 250, 'time_ms': 250, 'repeats': 1})

    # ------------------------------------------------------------------------------------------------------------------
    def getData(self, timeout=0.5):
        try:
            data = self.device.function(function='getData',
                                        data=None,
                                        return_type=dict,
                                        request_response=True,
                                        timeout=timeout)
        except TimeoutError:
            data = None
        return data

    # ------------------------------------------------------------------------------------------------------------------
    def addMotion(self, motion):
        ...

    # ------------------------------------------------------------------------------------------------------------------
    def setExternalLEDs(self, color):
        ...

    # ------------------------------------------------------------------------------------------------------------------
    def runSensingStep(self):
        ...

    # ------------------------------------------------------------------------------------------------------------------
    def runControlStep(self):
        ...

    # === PRIVATE METHODS ==============================================================================================
    def _onStream_callback(self, message, *args, **kwargs):
        ...
