import time

from RPi import GPIO
from control_board.stm32.stm32 import resetSTM32


def reset_uart(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 1)
    GPIO.output(pin, 0)
    # GPIO.cleanup()


if __name__ == '__main__':
    resetSTM32()
