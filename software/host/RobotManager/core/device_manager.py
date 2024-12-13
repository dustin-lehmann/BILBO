import time

from core.communication.wifi.tcp.protocols.tcp_json_protocol import TCP_JSON_Message
from core.communication.wifi.tcp.tcp_server import TCP_Server
from core.device import Device
from utils.callbacks import Callback
from utils.logging import Logger
from utils.network.network import getValidHostIP

logger = Logger('device manager')
logger.setLevel('INFO')


class DeviceManager:
    server: TCP_Server
    devices: dict[str, Device]
    callbacks: dict[str, list[Callback]]

    # === INIT =========================================================================================================
    def __init__(self):

        self.devices = {}

        self.callbacks = {
            'new_device': [],
            'device_disconnected': [],
            'stream': [],
        }

        address = getValidHostIP()
        if address is None:
            logger.info("No valid IP available")
            exit()

        self.server = TCP_Server(address)
        self.server.registerCallback('connected', self._newConnection_callback)

        self._unregistered_devices = []

    # === METHODS ======================================================================================================
    def registerCallback(self, callback_id, callback):
        if callback_id in self.callbacks.keys():
            self.callbacks[callback_id].append(callback)
        else:
            raise Exception(f"No callback with id {callback_id} is known.")

    # ------------------------------------------------------------------------------------------------------------------
    def init(self):
        ...

    # ------------------------------------------------------------------------------------------------------------------
    def start(self):
        logger.info(f"Starting Device Manager on {self.server.address}")
        self.server.start()

    # === PRIVATE METHODS ==============================================================================================
    def _newConnection_callback(self, connection):

        # Make a new generic device with the connection
        device = Device()
        device.connection = connection

        # Append this device to the unregistered devices, since it has not yet sent an identification message
        self._unregistered_devices.append(device)

        device.registerCallback('registered', self._deviceRegistered_callback)
        device.registerCallback('disconnected', self._deviceDisconnected_callback)
        logger.debug(f"New device connected. Address: {device.connection.address}, IP: {device.connection.ip}")

    # ------------------------------------------------------------------------------------------------------------------
    def _deviceRegistered_callback(self, device: Device):

        logger.info(
            f'New device registered. Name: {device.information.device_name} ({device.information.device_class}/{device.information.device_type})')

        self._sendSyncMessage(device)
        self.devices[device.information.device_id] = device
        self._unregistered_devices.remove(device)

        device.registerCallback('stream', self._deviceStreamCallback)
        device.registerCallback('event', self._deviceEventCallback)

        for callback in self.callbacks['new_device']:
            callback(device=device)

    # ------------------------------------------------------------------------------------------------------------------
    def _deviceDisconnected_callback(self, device):
        logger.info(
            f'Device disconnected. Name: {device.information.device_name} ({device.information.device_class}/{device.information.device_type})')
        for callback in self.callbacks['device_disconnected']:
            callback(device=device)

    # ------------------------------------------------------------------------------------------------------------------
    def _deviceStreamCallback(self, stream, device, *args, **kwargs):
        for callback in self.callbacks['stream']:
            callback(stream, device, *args, **kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    def _deviceEventCallback(self, message, device, *args, **kwargs):
        ...

    # ------------------------------------------------------------------------------------------------------------------
    def _sendSyncMessage(self, device: Device):

        message = TCP_JSON_Message()

        message.type = 'event'
        message.event = 'sync'
        message.data = {
            'time': time.time()
        }
        device.send(message)

    # ------------------------------------------------------------------------------------------------------------------
    def _sendHeartBeatMessage(self):
        message = TCP_JSON_Message()

        message.type = 'event'
        message.event = 'heartbeat'
        message.data = {
            'time': time.time()
        }
        for id, device in self.devices.items():
            device.send(message)
