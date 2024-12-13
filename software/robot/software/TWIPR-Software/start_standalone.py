import time

from robot.applications.standalone.joystick_control import StandaloneJoystickControl
from robot.twipr import TWIPR


def main():
    twipr = TWIPR(reset_stm32=False)
    joystick_control = StandaloneJoystickControl(twipr=twipr)
    twipr.init()
    joystick_control.init()
    twipr.start()
    joystick_control.start()


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        exit(0)



if __name__ == '__main__':
    main()
