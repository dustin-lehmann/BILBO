import threading
import time

from applications.FRODO.tracker.assets import TrackedAsset, TrackedVisionRobot, vision_robot_application_assets, \
    TrackedOrigin
from extensions.optitrack.optitrack import OptiTrack, RigidBodySample
from utils.callbacks import callback_handler, CallbackContainer
from utils.events import event_handler, ConditionEvent, EventListener
from utils.logging_utils import Logger
from utils.websockets.websockets import SyncWebsocketServer
from utils.time import IntervalTimer, Timer

# ======================================================================================================================
logger = Logger('Tracker')
logger.setLevel('INFO')


@callback_handler
class Tracker_Callbacks:
    new_sample: CallbackContainer
    description_received: CallbackContainer


@event_handler
class Tracker_Events:
    new_sample: ConditionEvent
    description_received: ConditionEvent


# ======================================================================================================================
class Tracker:
    assets: dict[str, TrackedAsset]
    optitrack: OptiTrack

    callbacks: Tracker_Callbacks
    events: Tracker_Events
    _websocket_update_time = 0.05
    _websocket_timer: Timer

    _exit: bool = False
    _thread: threading.Thread

    # === INIT =========================================================================================================
    def __init__(self, assets: dict[str, TrackedAsset] = vision_robot_application_assets, debug_stream: bool = False):

        self.assets = assets

        self.optitrack = OptiTrack(server_address="192.168.8.247")

        self.event_listener_sample = EventListener(self.optitrack.events.sample, callback=self._optitrack_new_sample_callback)

        # self.optitrack.callbacks.sample.register(self._optitrack_new_sample_callback)
        self.optitrack.callbacks.description_received.register(self._optitrack_description_callback)

        self.callbacks = Tracker_Callbacks()
        self.events = Tracker_Events()
        # self._thread = threading.Thread(target=self.task, daemon=True)

    # ------------------------------------------------------------------------------------------------------------------
    def init(self):
        self.optitrack.init()
        ...

    # ------------------------------------------------------------------------------------------------------------------
    def start(self):
        self.optitrack.start()
        logger.info("Starting Tracker")
        self.event_listener_sample.start()
        # self._thread.start()

    # ------------------------------------------------------------------------------------------------------------------
    def close(self, *args, **kwargs):
        self._exit = True

    # ------------------------------------------------------------------------------------------------------------------
    def task(self):

        while not self._exit:
            time.sleep(self._websocket_update_time)

    # === PRIVATE METHODS ==============================================================================================
    def _optitrack_new_sample_callback(self, sample: dict[str, RigidBodySample], *args, **kwargs):
        for name, asset in self.assets.items():

            # Extract the asset data
            if name not in sample:
                logger.error(f"Asset {name} not found in sample")
                continue

            asset_data = sample[name]
            asset.update(asset_data)

        self.callbacks.new_sample.call(self.assets)
        self.events.new_sample.set(self.assets)

    # ------------------------------------------------------------------------------------------------------------------
    def _optitrack_description_callback(self, rigid_bodies):

        all_assets_tracked = True
        # Check if all assets are currently tracked
        for name, asset in self.assets.items():
            if name not in rigid_bodies:
                logger.error(f"Asset {name} not available in OptiTrack data")
                all_assets_tracked = False

        if all_assets_tracked:
            logger.info("All assets tracked")

        self.callbacks.description_received.call(self.assets)
        self.events.description_received.set(self.assets)

    # ------------------------------------------------------------------------------------------------------------------
    def _websocket_debug_stream(self):
        ...


if __name__ == '__main__':
    tracker = Tracker(debug_stream=True)
    tracker.init()
    tracker.start()

    while True:
        time.sleep(1)
