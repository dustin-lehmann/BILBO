import RPi.GPIO as GPIO
import time
import sys
import os

# Add the top-level module to the Python path
top_level_module = os.path.expanduser("~/software")
if top_level_module not in sys.path:
    sys.path.insert(0, top_level_module)

from utils.button import Button
from control_board.config import getBoardConfig

config = getBoardConfig()

# GPIO setup
LED_PIN = config['pins']['RC_SIDE_BUTTON_LED']
BUTTON_PIN = config['pins']['RC_SIDE_BUTTON_PIN']

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, False)

# Initialize LED state
led_state = False


# Define callback functions
def toggle_led():
    global led_state
    led_state = not led_state
    GPIO.output(LED_PIN, led_state)
    print(f"LED {'ON' if led_state else 'OFF'}")


def long_press_detected():
    print("Long press detected")


# Create Button instance
button = Button(BUTTON_PIN, short_press_callback=None, long_press_callback=toggle_led)

try:
    print("Press the button to toggle the LED (short press) or trigger a long press.")
    while True:
        time.sleep(0.1)  # Keep the program running

except KeyboardInterrupt:
    print("\nExiting program...")

finally:
    button.stop()
    GPIO.cleanup()
    print("GPIO cleaned up.")
