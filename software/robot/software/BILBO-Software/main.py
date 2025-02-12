import time

from robot.bilbo import BILBO
from robot.control.definitions import BILBO_Control_Mode
from utils.static_variable import StaticVariable
from utils.events import EventListener
from utils.callbacks import Callback
from utils.logging_utils import setLoggerLevel

setLoggerLevel('wifi', 'ERROR')


def main():
    bilbo = BILBO()
    bilbo.init()
    bilbo.start()

    time.sleep(2)
    bilbo.control.setMode(BILBO_Control_Mode.BALANCING)
    time.sleep(3)
    bilbo.control.setMode(BILBO_Control_Mode.OFF)

    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
