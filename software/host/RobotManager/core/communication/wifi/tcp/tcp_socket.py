import threading
import time
import socket
import queue
import dataclasses

import cobs.cobs as cobs

from utils.callbacks import callback_handler, CallbackContainer
from utils.logging_utils import Logger

logger = Logger('tcp')
logger.setLevel('INFO')

PACKAGE_TIMEOUT_TIME = 5
FAULTY_PACKAGES_MAX_NUMBER = 10


time1 = 0

@dataclasses.dataclass
class FaultyPackage:
    timestamp: float


@callback_handler
class TCPSocketCallbacks:
    rx: CallbackContainer
    disconnected: CallbackContainer


class TCP_Socket:
    address: str  # IP address of the client
    rx_queue: queue.Queue  # Queue of incoming messages from the client
    tx_queue: queue.Queue  # Queue of outgoing messages to the client
    config: dict

    rx_callback: callable  # Callback function that is called as soon as a message is received
    rx_event: threading.Event

    _connection: socket.socket
    _rxThread: threading.Thread
    _faultyPackages: list
    _rx_buffer: bytes  # Buffer for accumulating partial data
    _last_faulty_cleanup: float

    def __init__(self, connection: socket.socket, address: str):
        self._connection = connection
        self.address = address

        self.config = {
            'delimiter': b'\x00',
            'cobs': True
        }

        self.rx_queue = queue.Queue()
        self.tx_queue = queue.Queue()

        self._exit = False

        self.callbacks = TCPSocketCallbacks()

        self.rx_event = threading.Event()

        self._faultyPackages = []
        self._rx_buffer = b''
        self._last_faulty_cleanup = time.time()

        self._rxThread = threading.Thread(target=self._rx_thread_fun, daemon=True)
        self._rxThread.start()

    def send(self, data):
        """Encode and send data immediately over the socket."""
        global time1
        data = self._prepareTxData(data)
        self._write(data)

    def rxAvailable(self):
        return self.rx_queue.qsize()

    def close(self):
        try:
            self._connection.close()
        except Exception:
            pass
        self._exit = True
        logger.info("TCP socket %s closed", self.address)
        for callback in self.callbacks.disconnected:
            callback(self)

    def setConfig(self, config):
        """Merge new config parameters with existing config."""
        self.config = {**self.config, **config}

    def _rx_thread_fun(self):
        while not self._exit:
            try:
                data = self._connection.recv(8092)
            except Exception as e:
                logger.warning("Error in TCP connection: %s. Closing connection.", e)
                self.close()
                return

            # If no data, the client closed the connection.
            if not data:
                self.close()
                break

            # print(f"time: {((time.perf_counter() - time1)*1000):.1f} ms")
            self._processRxData(data)

            # Clean up old faulty packages approximately once per second.
            now = time.time()
            if int(now - self._last_faulty_cleanup) > 1:
                self._faultyPackages = [
                    p for p in self._faultyPackages if now < (p.timestamp + PACKAGE_TIMEOUT_TIME)
                ]
                if len(self._faultyPackages) > FAULTY_PACKAGES_MAX_NUMBER:
                    logger.warning("Received %d faulty TCP packages in the last %d seconds",
                                   FAULTY_PACKAGES_MAX_NUMBER, PACKAGE_TIMEOUT_TIME)
                self._last_faulty_cleanup = now

    def _prepareTxData(self, data):
        if isinstance(data, list):
            data = bytes(data)
        if self.config.get('cobs', False):
            data = cobs.encode(data)
        if self.config.get('delimiter') is not None:
            data += self.config['delimiter']
        return data

    def _write(self, data):
        try:
            self._connection.sendall(data)
        except Exception as e:
            logger.warning("Error sending data: %s", e)
            self.close()

    def _processRxData(self, data):
        """
        Append new data to the internal buffer and extract complete packets.
        Incomplete data remains in the buffer until more data arrives.
        """
        self._rx_buffer += data
        delimiter = self.config.get('delimiter')
        while True:
            index = self._rx_buffer.find(delimiter)
            if index == -1:
                # No complete packet found yet.
                break
            # Extract one complete packet.
            packet = self._rx_buffer[:index]
            self._rx_buffer = self._rx_buffer[index + len(delimiter):]
            if self.config.get('cobs', False):
                try:
                    packet = cobs.decode(packet)
                except Exception:
                    self._faultyPackages.append(FaultyPackage(timestamp=time.time()))
                    continue  # Skip this packet if it fails to decode.
            self.rx_queue.put(packet)

        # If any packets were added, signal and call rx callbacks.
        if not self.rx_queue.empty():
            self.rx_event.set()
            for callback in self.callbacks.rx:
                callback(self)


@callback_handler
class TCPSocketsHandlerCallbacks:
    client_connected: CallbackContainer
    client_disconnected: CallbackContainer
    server_error: CallbackContainer


class TCP_SocketsHandler:
    address: str
    port: int
    sockets: list  # List of the connected clients
    _thread: threading.Thread
    _server: socket.socket
    config: dict
    callbacks: TCPSocketsHandlerCallbacks
    _exit: bool

    def __init__(self, address, hostname: bool = False, config: dict = None):
        default_config = {
            'max_clients': 100,
            'port': 6666,
        }
        if config is None:
            config = {}
        self.config = {**default_config, **config}

        self.sockets = []
        self.address = address
        self.port = self.config['port']
        self.callbacks = TCPSocketsHandlerCallbacks()
        self._exit = False

        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def init(self):
        # Placeholder for any additional initialization.
        pass

    def start(self):
        self._thread = threading.Thread(target=self._threadFunction, daemon=True)
        self._thread.start()

    def close(self):
        logger.info("TCP host closed on %s:%d", self.address, self.port)
        self._exit = True
        try:
            self._server.close()
        except Exception:
            pass
        if self._thread.is_alive():
            self._thread.join()

    def send(self):
        # Placeholder: Implement sending to all or a particular client if needed.
        pass

    def _threadFunction(self):
        server_address = (self.address, self.port)
        try:
            self._server.bind(server_address)
        except OSError as e:
            raise Exception("Address already in use. Please wait until the address is released") from e

        self._server.listen(self.config['max_clients'])
        logger.info("Starting TCP host on %s:%d", self.address, self.port)

        while not self._exit:
            try:
                connection, client_address = self._server.accept()
                self._acceptNewClient(connection, client_address)
            except Exception as e:
                if not self._exit:
                    logger.warning("Error accepting new client: %s", e)
                    for callback in self.callbacks.server_error:
                        callback(e)

    def _acceptNewClient(self, connection, address):
        client = TCP_Socket(connection, address)
        self.sockets.append(client)
        logger.info("New client connected: %s", client.address)
        client.callbacks.disconnected.register(self._clientClosed_callback)
        for callback in self.callbacks.client_connected:
            callback(client)

    def _clientClosed_callback(self, client: TCP_Socket):
        if client in self.sockets:
            self.sockets.remove(client)
        for cb in self.callbacks.client_disconnected:
            cb(client)
