import time

from robot.control.twipr_control import TWIPR_Control_Mode
from robot.twipr import TWIPR


def main():
    twipr = TWIPR(reset_stm32=False)
    twipr.init()
    twipr.start()


if __name__ == '__main__':
    main()
