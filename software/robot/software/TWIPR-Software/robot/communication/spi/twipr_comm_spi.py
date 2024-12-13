import time
from ctypes import sizeof

from core.communication.spi.spi import SPI_Interface
from utils.callbacks import Callback
from utils.exit import ExitHandler
from robot.definitions.stm32_sample import twipr_stm32_sample
from utils.ctypes_utils import bytes_to_value
from robot.definitions.stm32_sample import SAMPLE_BUFFER_SIZE

from RPi import GPIO

last_time = 0


class TWIPR_SPI_Interface:
    interface: SPI_Interface
    callbacks: dict
    sample_notification_pin: int

    def __init__(self, interface: SPI_Interface, sample_notification_pin):
        self.interface = interface
        self.sample_notification_pin = sample_notification_pin
        self.callbacks = {
            'rx_samples': []
        }

        self.exit = ExitHandler()
        self.exit.register(self.close)

    # === METHODS ======================================================================================================
    def registerCallback(self, callback_id, function: callable, parameters: dict = None, lambdas: dict = None,
                         **kwargs):
        callback = Callback(function, parameters, lambdas, **kwargs)

        if callback_id in self.callbacks:
            self.callbacks[callback_id].append(callback)
        else:
            raise Exception("Invalid Callback type")

    def init(self):
        self._configureSampleGPIO()
        ...

    def start(self):
        ...

    def close(self):
        ...
        GPIO.cleanup()

    # === PRIVATE METHODS ==============================================================================================

    def _configureSampleGPIO(self):
        time.sleep(0.25)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sample_notification_pin, GPIO.IN,
                   pull_up_down=GPIO.PUD_DOWN)  # pull_up_down=GPIO.PUD_DOWN
        GPIO.add_event_detect(self.sample_notification_pin, GPIO.BOTH,
                              callback=self._samplesReadyInterrupt, bouncetime=1)
        # try:
        #     GPIO.add_event_detect(self.sample_notification_pin, GPIO.BOTH,
        #                           callback=self._samplesReadyInterrupt, bouncetime=1)
        # except RuntimeError:
        #     GPIO.add_event_detect(self.sample_notification_pin, GPIO.BOTH,
        #                           callback=self._samplesReadyInterrupt, bouncetime=1)

    # ------------------------------------------------------------------------------------------------------------------
    def _samplesReadyInterrupt(self, *args, **kwargs):
        global last_time
        # time_current = time.perf_counter()
        new_samples = self._readSamples()
        # print(new_samples[0])

        # print(f"Time Difference: {abs(100-(time_current - last_time)*1000)}")
        # last_time = time_current

        for callback in self.callbacks['rx_samples']:
            callback(new_samples)

    # ------------------------------------------------------------------------------------------------------------------
    def _readSamples(self):
        data_rx_bytes = bytearray(SAMPLE_BUFFER_SIZE * sizeof(twipr_stm32_sample))
        self.interface.readinto(data_rx_bytes, start=0,
                                end=SAMPLE_BUFFER_SIZE * sizeof(twipr_stm32_sample))
        samples = []
        for i in range(0, SAMPLE_BUFFER_SIZE):
            sample = bytes_to_value(
                byte_data=data_rx_bytes[i * sizeof(twipr_stm32_sample):(i + 1) * sizeof(twipr_stm32_sample)],
                ctype_type=twipr_stm32_sample)
            samples.append(sample)

        return samples
