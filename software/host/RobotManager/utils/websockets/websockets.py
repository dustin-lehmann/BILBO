import threading

from websocket_server import WebsocketServer
import json
from utils.exit import ExitHandler


class SyncWebsocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = WebsocketServer(host=self.host, port=self.port)
        self.clients = []  # Store connected clients
        self.message_callback = None
        self.connection_callback = None
        self.running = False
        self.thread = None

        # Exit handling
        self.exit_handler = ExitHandler()
        self.exit_handler.register(self.stop)

    def start(self):
        """
        Start the WebSocket server in a separate thread (non-blocking).
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_server, daemon=True)
            self.thread.start()

    def _run_server(self):
        """
        Run the WebSocket server (blocking call). Should be run in a separate thread.
        """
        # Attach callbacks
        self.server.set_fn_new_client(self._on_new_client)
        self.server.set_fn_client_left(self._on_client_left)
        self.server.set_fn_message_received(self._on_message_received)

        try:
            self.server.run_forever()
        except Exception as e:
            ...
            # print(f"Error in server loop: {e}")
        finally:
            self.running = False

    def _on_new_client(self, client, server):
        self.clients.append(client)  # Add client to the list
        if self.connection_callback:
            self.connection_callback(client)

    def _on_client_left(self, client, server):
        if client in self.clients:
            self.clients.remove(client)  # Remove client from the list

    def _on_message_received(self, client, server, message):
        if self.message_callback:
            self.message_callback(message, client)

    def send(self, message):
        """
        Send a message to all connected clients.
        """
        if isinstance(message, dict):
            message = json.dumps(message)
        for client in self.clients:
            self.server.send_message(client, message)

    def stop(self, *args, **kwargs):
        """
        Stop the WebSocket server.
        """
        if self.running:
            self.server.shutdown()
            if self.thread:
                self.thread.join()
            self.running = False

    def set_message_callback(self, callback):
        self.message_callback = callback

    def set_connection_callback(self, callback):
        self.connection_callback = callback
