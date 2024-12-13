import json

import numpy as np

from scioi_py_core.objects.twipr.environment_base import EnvironmentBase
from scioi_py_core.objects.twipr.EnvironmentTWIPR_objects import TWIPR_Agent
from scioi_py_core.objects.world import floor
from scioi_py_core.utils.babylon import setBabylonSettings
import scioi_py_core.core as core

wait_steps = 100

padding = 1000


class Environment_CDC_Animation_Estimation(EnvironmentBase):
    agent1: TWIPR_Agent

    data: dict
    k: int

    def __init__(self, experiment, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open('./Experiment_evaluation/estimation_out_to_python.json') as data_file:
            data = json.load(data_file)

        webapp_title = ''

        self.experiment_len = len(data['t'])
        self.agent_1_data = {
            'x': [data['x'][0][0]] * padding + data['x'][0],
            'y': [0] * (self.experiment_len + padding),
            'psi': [0] * (self.experiment_len + padding),
            'theta': [data['x'][2][0]] * padding + data['x'][2]
        }

        setBabylonSettings(title=webapp_title)

        self.agent1 = TWIPR_Agent(world=self.world, agent_id=0, speed_control=False)

        self.agent1.setPosition(x=-1.2)

        fl1 = floor.generateTileFloor(self.world, tiles=[6, 1], tile_size=0.4)

        self.k = 0

    def action_input(self, *args, **kwargs):
        super().action_input(*args, **kwargs)
        if self.k < self.experiment_len + padding:
            self.agent1.setConfiguration([[self.agent_1_data['x'][self.k], self.agent_1_data['y'][self.k]],
                                          self.agent_1_data['theta'][self.k],
                                          self.agent_1_data['psi'][self.k]])

        self.k = self.k + 1


class Environment_CDC_Animation_Transfer(EnvironmentBase):
    agent1: TWIPR_Agent

    data: dict
    k: int

    def __init__(self, experiment, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open('./Experiment_evaluation/transfer_out_to_python.json') as data_file:
            data = json.load(data_file)

        webapp_title = ''

        self.x_offset = -0.6

        self.experiment_len = len(data['t']) - 200
        self.agent_1_data = {
            'x': np.asarray([data['x'][0][0]] * padding + data['x'][0]) + self.x_offset,
            'y': [0] * (self.experiment_len + padding),
            'psi': [0] * (self.experiment_len + padding),
            'theta': [data['x'][2][0]] * padding + data['x'][2]
        }

        setBabylonSettings(title=webapp_title)

        self.agent1 = TWIPR_Agent(world=self.world, agent_id=0, speed_control=False)
        self.agent1.setPosition(x=self.x_offset)

        fl1 = floor.generateTileFloor(self.world, tiles=[6, 1], tile_size=0.4)
        #
        group1 = core.world.WorldObjectGroup(name='Gate', world=self.world, local_space=core.spaces.Space3D())

        post_height = 0.13
        group_object1 = core.obstacles.CuboidObstacle_3D(group=group1, size_x=0.04, size_y=0.04, size_z=post_height,
                                                         position=[0, 0.2, post_height/2])
        group_object2 = core.obstacles.CuboidObstacle_3D(group=group1, size_x=0.04, size_y=0.04, size_z=post_height,
                                                         position=[0, -0.2, post_height/2])
        group_object3 = core.obstacles.CuboidObstacle_3D(group=group1, size_x=0.04, size_y=0.44, size_z=0.04,
                                                         position=[0, 0, post_height+0.04/2])

        group1.setPosition(x=-0.4)

        self.k = 0

    def action_input(self, *args, **kwargs):
        super().action_input(*args, **kwargs)
        if self.k < self.experiment_len + padding:
            self.agent1.setConfiguration(
                [[self.agent_1_data['x'][self.k] * 0.5 + self.x_offset, self.agent_1_data['y'][self.k]],
                 self.agent_1_data['theta'][self.k],
                 self.agent_1_data['psi'][self.k]])

        self.k = self.k + 1


def main():
    env = Environment_CDC_Animation_Transfer(experiment='transfer', visualization='babylon',
                                             webapp_config={'title': 'Direct Transfer',
                                                            'record': {'file': 'transfer.webm', 'time': 20},
                                                            'background': [1, 1, 1]})
    setBabylonSettings(background_color=[1, 1, 1])
    env.init()
    env.start()
    ...


if __name__ == '__main__':
    main()
