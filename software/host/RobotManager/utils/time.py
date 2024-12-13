from typing import Callable

from utils.callbacks import Callback
from threading import Timer as ThreadTimer


class Timer:
    _reset_time: float

    timeout: float
    repeat: bool

    _callbacks: dict[str, list]
    _threadTimer: ThreadTimer

    _stop: bool

    def __init__(self):
        self._reset_time = time.time()
        self.timeout = None
        self.repeat = False

        self._threadTimer = None

        self._callbacks = {
            'timeout': []
        }

    # ------------------------------------------------------------------------------------------------------------------
    def registerCallback(self, callback_id, function: callable, parameters: dict = None, lambdas: dict = None,
                         **kwargs):
        callback = Callback(function, parameters, lambdas, **kwargs)

        if callback_id in self._callbacks:
            self._callbacks[callback_id].append(callback)
        else:
            raise Exception("Invalid Callback type")

    # ------------------------------------------------------------------------------------------------------------------

    def start(self, timeout=None, repeat: bool = True):
        self.reset()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def time(self):
        return time.time() - self._reset_time

    # ------------------------------------------------------------------------------------------------------------------
    def reset(self):
        self._reset_time = time.time()
        if self._threadTimer is not None:
            self._threadTimer.cancel()
            self._threadTimer = ThreadTimer(self.timeout, self._timeout_callback)
            self._threadTimer.start()

    # ------------------------------------------------------------------------------------------------------------------
    def stop(self):
        self._threadTimer.cancel()
        self._threadTimer = None

    # ------------------------------------------------------------------------------------------------------------------
    def set(self, value):
        self._reset_time = time.time() - value

    def _timeout_callback(self):
        for callback in self._callbacks['overflow']:
            callback()

        if self.repeat:
            self._threadTimer = ThreadTimer(self.timeout, self._timeout_callback)
            self._threadTimer.start()
        else:
            self._threadTimer = None

    # ------------------------------------------------------------------------------------------------------------------
    def __gt__(self, other):
        return self.time > other

    # ------------------------------------------------------------------------------------------------------------------
    def __lt__(self, other):
        return self.time < other


def sleep(seconds):
    precise_sleep(seconds)


def precise_sleep(seconds: float):
    """
    High-precision sleep function.
    """
    target_time = time.perf_counter() + seconds

    # Coarse sleep until close to the target time
    while True:
        remaining = target_time - time.perf_counter()
        if remaining <= 0:
            break
        if remaining > 0.001:  # If more than 1ms remains, sleep briefly
            time.sleep(remaining / 2)  # Use fractional sleep to avoid overshooting
        else:
            break

    # Busy-wait for the final few microseconds
    while time.perf_counter() < target_time:
        pass

import threading
import time


# ----------------------------------------------------------------------------------------------------------------------
class TimeoutTimer:
    def __init__(self, timeout_time, timeout_callback):
        """
        Initializes the TimeoutTimer.

        :param timeout_time: The timeout duration in seconds.
        :param timeout_callback: The callback function to execute on timeout.
        """
        self.timeout_time = timeout_time
        self.timeout_callback = timeout_callback
        self._last_reset_time = time.time()
        self._stop_event = threading.Event()
        self._timer_thread = threading.Thread(target=self._run_timer, daemon=True)
        self._timer_thread.start()

    def _run_timer(self):
        """The method executed by the timer thread."""
        while not self._stop_event.is_set():
            # Check if the current time has exceeded the timeout time.
            if time.time() - self._last_reset_time >= self.timeout_time:
                self.timeout_callback()
                # Wait for the timer to be reset or stopped
                while time.time() - self._last_reset_time >= self.timeout_time:
                    if self._stop_event.is_set():
                        return
                    time.sleep(0.1)
            time.sleep(0.1)  # Small sleep to avoid high CPU usage.

    def reset(self):
        """
        Resets the timer by updating the last reset time.
        """
        self._last_reset_time = time.time()

    def stop(self):
        """
        Stops the timer thread.
        """
        self._stop_event.set()
        self._timer_thread.join()


class DelayedExecutor:
    def __init__(self, func: Callable, delay: float, *args, **kwargs):
        """
        Initialize the DelayedExecutor.

        :param func: The function to execute.
        :param delay: Time in seconds to wait before executing the function.
        :param args: Positional arguments for the function.
        :param kwargs: Keyword arguments for the function.
        """
        self.func = func
        self.delay = delay
        self.args = args
        self.kwargs = kwargs

    def start(self):
        """
        Start the delayed execution in a separate thread.
        """
        thread = threading.Thread(target=self._delayed_run)
        thread.daemon = True  # Ensures the thread exits when the main program exits
        thread.start()

    def _delayed_run(self):
        """
        Wait for the specified delay and then execute the function.
        """
        time.sleep(self.delay)
        self.func(*self.args, **self.kwargs)


def delayed_execution(func: Callable, delay: float, *args, **kwargs) -> None:
    """
    Execute a function after a specified delay in a non-blocking manner.

    :param func: The function to execute.
    :param delay: Time in seconds to wait before executing the function.
    :param args: Positional arguments for the function.
    :param kwargs: Keyword arguments for the function.
    """
    executor = DelayedExecutor(func, delay, *args, **kwargs)
    executor.start()


# Example usage:
if __name__ == "__main__":
    def on_timeout():
        print("Timeout occurred!")

    # Create a TimeoutTimer with a 5-second timeout.
    timer = TimeoutTimer(5, on_timeout)
    time.sleep(3)
    timer.reset()
    time.sleep(3)
    timer.reset()
    time.sleep(7)
    # Simulate heartbeat activity.
    # try:
    #     while True:
    #         print("Heartbeat received. Resetting timer.")
    #         timer.reset()
    #         time.sleep(3)  # Simulate heartbeat intervals.
    # except KeyboardInterrupt:
    #     print("Stopping timer.")
    #     timer.stop()