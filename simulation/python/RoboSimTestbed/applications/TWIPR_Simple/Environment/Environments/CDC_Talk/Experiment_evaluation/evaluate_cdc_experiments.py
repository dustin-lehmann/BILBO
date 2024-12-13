import numpy as np
from matplotlib import pyplot as plt
from scipy.io import savemat

from json_helpers import readJSON, writeJSON
from utils import getSignal

Ts = 0.01


def evaluate_direct():
    data = readJSON("./free_experiment_new_direct_1.json")

    tick = np.asarray(getSignal(data, 'general', 'tick'))
    time = (tick - tick[0]) * Ts
    theta = getSignal(data, 'estimation', 'state', 'theta')

    output_data = {
        't': time,
        'theta': theta,
    }

    savemat("output_to_matlab_direct.mat", output_data)

    plt.plot(time, theta)
    plt.show()
    pass


def evaluate_transfer():
    data = readJSON("./free_experiment_new_dive_1.json")

    tick = np.asarray(getSignal(data, 'general', 'tick'))
    time = (tick - tick[0]) * Ts
    theta = getSignal(data, 'estimation', 'state', 'theta')
    u = getSignal(data, 'control', 'input', 'u1')

    output_data = {
        't': time,
        'theta': theta,
        'u': u,
    }

    savemat("output_to_matlab_dive.mat", output_data)

    plt.plot(time, u)
    plt.show()


def evaluate_estimation():
    data = readJSON("./estimation_output.json")

    tick = np.asarray(getSignal(data['samples_experiment'], 'general', 'tick'))
    time = (tick - tick[0]) * Ts
    theta = getSignal(data['samples_experiment'], 'estimation', 'state', 'theta')
    u = data['u_est']

    output_data = {
        't': time,
        'u': u
    }

    # writeJSON('./output_to_matlab_estimation.json', output_data)
    savemat("output_to_matlab_estimation.mat", data)
    plt.plot(time, theta)
    plt.show()


if __name__ == '__main__':
    # evaluate_direct()
    evaluate_transfer()
    # evaluate_estimation()
