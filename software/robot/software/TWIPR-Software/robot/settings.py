import os

from utils.json_utils import writeJSON, readJSON

settings_file_path = os.path.expanduser('~/robot_settings.json')


# # 'balancing_gain': [0.035, 0.06, 0.01, 0.009,
# #                    0.035, 0.06, 0.01, -0.009],
# # 'balancing_gain': [0.08, 0.1, 0.02, 0.009,
# #                    0.08, 0.1, 0.02, -0.009],
# 'balancing_gain'
#
#
# # 'balancing_gain': [0.1, 0.2, 0.04, 0.036,
# #                    0.1, 0.2, 0.04, -0.036],

def generate_settings_file():
    settings = {
        'id': 'bilbo2',
        'name': 'BILBO 2',
        'control': {
            'feedback_gain': [0.12, 0.24, 0.04, 0.036,
                              0.12, 0.24, 0.04, -0.036],
            'pid_forward': {
                'P': -0.06,
                'I': -0.09,
                'D': 0
            },
            'pid_turn': {
                'P': -0.01,
                'I': -0.12,
                'D': 0.0
            },
            'theta_offset': 0,
            'torque_offset': [0, 0]
        },
        'external_inputs': {
            'normalized_torque_scale': {
                'forward': 0.3,
                'turn': 0.3
            },
            'normalized_velocity_scale': {
                'forward': 1,
                'turn': 5,
            }
        },
        'safety': {
            'max_wheel_speed': 100,
        }
    }

    if os.path.isfile(settings_file_path):
        os.remove(settings_file_path)

    writeJSON(settings_file_path, settings)


def readSettings():
    settings = readJSON(settings_file_path)
    return settings


if __name__ == '__main__':
    generate_settings_file()

