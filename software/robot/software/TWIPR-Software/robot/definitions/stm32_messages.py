import ctypes
from core.communication.serial.serial_interface import SerialCommandType, addSerialMessage
from utils.callbacks import Callback
from utils.logging_utils import Logger
from robot.definitions.stm32_errors import TWIPR_SupervisorErrorCodes, TWIPR_ErrorCode

supervisor_logger = Logger('supervisor')
supervisor_logger.setLevel('INFO')

# ======================================================================================================================
# INCOMING MESSAGES
# ======================================================================================================================
# Events
# ======================================================================================================================
TWIPR_MESSAGE_PRINT_WARNING = 0x0301
@addSerialMessage
class TWIPR_WarningMessage:
    @classmethod
    def printWarningMessage(cls, message, *args, **kwargs):
        supervisor_logger.warning(f"{TWIPR_ErrorCode(message.data['error']).name}: ID {TWIPR_SupervisorErrorCodes(message.data['id']).name}: {message.data['text'].decode('utf-8')}")

    command: SerialCommandType = SerialCommandType.UART_CMD_EVENT
    address: int = TWIPR_MESSAGE_PRINT_WARNING
    callback: Callback = printWarningMessage
    class data_type(ctypes.Structure):
        _fields_ = [("id", ctypes.c_uint8), ("error", ctypes.c_uint8), ("text", ctypes.c_char*50), ]


# ======================================================================================================================