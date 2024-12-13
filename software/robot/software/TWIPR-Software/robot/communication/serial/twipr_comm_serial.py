from core.communication.serial.serial_interface import Serial_Interface

import robot.definitions.stm32_addresses as addresses
from robot.definitions.stm32_general import twipr_firmware_revision
from robot.definitions.stm32_messages import *


class TWIPR_Serial_Interface:
    interface: Serial_Interface
    callbacks: dict

    def __init__(self, interface: Serial_Interface):
        self.interface = interface

        self.interface.registerCallback('rx', self._rx_callback)

        self.callbacks = {
            'rx': [],
            'rx_event': [],
            'rx_error': [],
            'rx_debug': [],
        }

    # === METHODS ======================================================================================================
    def registerCallback(self, callback_id, function: callable, parameters: dict = None, lambdas: dict = None,
                         **kwargs):
        callback = Callback(function, parameters, lambdas, **kwargs)

        if callback_id in self.callbacks:
            self.callbacks[callback_id].append(callback)
        else:
            raise Exception("Invalid Callback type")

    # ------------------------------------------------------------------------------------------------------------------
    def init(self):
        self.interface.init()

    # ------------------------------------------------------------------------------------------------------------------
    def start(self):
        self.interface.start()

    # ------------------------------------------------------------------------------------------------------------------
    def writeValue(self, module: int = 0, address: (int, list) = None, value=None, type=ctypes.c_uint8):
        self.interface.write(module, address, value, type)

    # ------------------------------------------------------------------------------------------------------------------
    def readValue(self, address:int, module: int = 0, type=ctypes.c_uint8):
        return self.interface.read(address, module, type)

    # ------------------------------------------------------------------------------------------------------------------
    def executeFunction(self, address, module: int = 0, data=None, input_type=None, output_type=None, timeout=1):
        return self.interface.function(address, module, data, input_type, output_type, timeout)

    # ------------------------------------------------------------------------------------------------------------------
    def readTick(self):
        tick = self.interface.read(module=addresses.TWIPR_AddressTables.REGISTER_TABLE_GENERAL,
                                   address=addresses.TWIPR_GeneralAddresses.ADDRESS_FIRMWARE_TICK,
                                   type=ctypes.c_uint32)

        return tick

    # ------------------------------------------------------------------------------------------------------------------
    def readFirmwareRevision(self):
        revision = self.interface.read(module=addresses.TWIPR_AddressTables.REGISTER_TABLE_GENERAL,
                                       address=addresses.TWIPR_GeneralAddresses.ADDRESS_FIRMWARE_REVISION,
                                       type=twipr_firmware_revision)

        return revision
    # ------------------------------------------------------------------------------------------------------------------
    def debug(self, state):
        self.interface.function(module=addresses.TWIPR_AddressTables.REGISTER_TABLE_GENERAL,
                                address=addresses.TWIPR_GeneralAddresses.ADDRESS_FIRMWARE_DEBUG,
                                data=state,
                                input_type=ctypes.c_uint8)

    # === PRIVATE METHODS ==============================================================================================
    def _rx_callback(self, message: SerialMessage, *args, **kwargs):
        message.executeCallback()