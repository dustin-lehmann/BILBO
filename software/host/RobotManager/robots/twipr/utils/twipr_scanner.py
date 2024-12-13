from robots.twipr.twipr_definitions import TWIPR_IDS
from utils.exit import ExitHandler
from utils.network.network import pingAddresses, resolveHostname
import threading
import time


class TWIPR_Scanner:
    def __init__(self, robot_ids, scan_interval=3):
        """
        Initializes the TWIPR_Scanner class.

        :param robot_ids: List of robot hostnames to scan.
        :param scan_interval: Time interval (in seconds) between scans.
        :param on_new_robot: Callback for when a new robot is detected.
        :param on_robot_lost: Callback for when a robot is no longer reachable.
        :param on_exit: Callback for when the scanner exits.
        """
        self.robot_ids = robot_ids
        self.scan_interval = scan_interval

        self.active_robots = {}  # {hostname: ip}
        self.scanning = False
        self._lock = threading.Lock()
        self._thread = None

        self.callbacks = {
            'robot_found': [],
            'robot_lost': []
        }

        self.exit_handler = ExitHandler()
        self.exit_handler.register(self.stop)

    # ==================================================================================================================
    def registerCallback(self, callback_id, callback):
        if callback_id in self.callbacks.keys():
            self.callbacks[callback_id].append(callback)
        else:
            raise Exception(f"No callback with id {callback_id} is known.")

    # ------------------------------------------------------------------------------------------------------------------
    def _scan_network(self):
        while self.scanning:
            reachable_robots = pingAddresses(self.robot_ids)
            with self._lock:
                # Detect newly active robots
                for hostname, is_reachable in reachable_robots.items():
                    if is_reachable and hostname not in self.active_robots:
                        ip_address = resolveHostname(hostname)
                        if ip_address:
                            self.active_robots[hostname] = ip_address
                            for callback in self.callbacks['robot_found']:
                                callback(hostname, ip_address)

                # Detect lost robots
                for hostname in list(self.active_robots.keys()):
                    if not reachable_robots.get(hostname, False):
                        ...
                        # for callback in self.callbacks['robot_lost']:
                        #     callback(hostname, ip_address)

                        # del self.active_robots[hostname]

            time.sleep(self.scan_interval)

    def start(self):
        """Starts the scanning process."""
        if not self.scanning:
            self.scanning = True
            self._thread = threading.Thread(target=self._scan_network)
            self._thread.start()

    def stop(self, *args, **kwargs):
        """Stops the scanning process."""
        if self.scanning:
            self.scanning = False
            if self._thread:
                self._thread.join()

    def get_active_robots(self):
        """Returns a dictionary of active robots."""
        with self._lock:
            return dict(self.active_robots)


if __name__ == '__main__':

    scanner = TWIPR_Scanner(
        robot_ids=TWIPR_IDS,
        scan_interval=3,
    )
    scanner.start()

    while True:
        time.sleep(10)
