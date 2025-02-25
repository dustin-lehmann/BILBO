import time


def main():
    babylon = BabylonVisualization(show='chromium')
    babylon.init()
    babylon.start()

    babylon.addObject('twipr1', 'BILBO', {'color': [0, 1, 0]})
    babylon.addObject('twipr2', 'BILBO', {'color': [1, 0, 0]})
    babylon.addObject('twipr3', 'BILBO', {'color': [0, 0, 1]})
    time.sleep(5)
    babylon.updateObject('twipr1', {'position': {'x': 1, 'y': 0}})
    babylon.updateObject('twipr2', {'position': {'x': 1, 'y': 0.5}})
    babylon.updateObject('twipr3', {'position': {'x': 1, 'y': 1}})

    time.sleep(1)
    x = 0
    while True:
        x = x+0.01
        time.sleep(0.01)


if __name__ == '__main__':
    main()
