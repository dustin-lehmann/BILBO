import os
import sys
import time

top_level_module = os.path.expanduser("~/software")
if top_level_module not in sys.path:
    sys.path.insert(0, top_level_module)

from robot.applications.standalone.joystick_control import StandaloneJoystickControl
from robot.twipr import TWIPR


def run_standalone():
    twipr = TWIPR(reset_stm32=False)
    joystick_control = StandaloneJoystickControl(twipr=twipr)
    twipr.init()
    joystick_control.init()
    twipr.start()
    joystick_control.start()


if __name__ == '__main__':
    run_standalone()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        exit(1)
