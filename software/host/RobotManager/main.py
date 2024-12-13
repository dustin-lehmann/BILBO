import time

from applications.TWIPR.general.JoystickControl import SimpleTwiprJoystickControl


def main():
    app = SimpleTwiprJoystickControl()
    app.init()
    app.start()

    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
