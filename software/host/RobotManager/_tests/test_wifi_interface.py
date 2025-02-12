import time

from applications.BILBO.general.JoystickControl import SimpleTwiprJoystickControl
from robots.twipr.twipr import TWIPR

bilbo1: TWIPR = None


def robot_callback(robot: TWIPR, event: str):
    global bilbo1
    if event == 'disconnect':
        print("Robot Disconnected")
        bilbo1 = None
    elif event == 'connect':
        print("Robot Connected")
        bilbo1 = robot


def main():
    app = SimpleTwiprJoystickControl()
    app.init()
    app.start()

    app.robot_manager.callbacks.new_robot.register(robot_callback, parameters={'event': 'connect'})
    app.robot_manager.callbacks.robot_disconnected.register(robot_callback, parameters={'event': 'disconnect'})

    while True:
        if bilbo1:
            print("Call Function")
            output = bilbo1.device.function(function='testfunction',
                                            data={
                                                'input1': 14,
                                                'input2': 'hallo'
                                            },
                                            request_response=True,
                                            timeout=1)
        time.sleep(3)


if __name__ == '__main__':
    main()
