from applications.SS24_Project_Cooperative_Sensing.definitions.coop_sens_agents import CoopSensAgent
from applications.SS24_Project_Cooperative_Sensing.definitions.coop_sens_environment import \
    EnvironmentBase_CooperativeSensing


class CoopSens_Example_Environment_1(EnvironmentBase_CooperativeSensing):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agent1 = CoopSensAgent(name='Agent 1', world=self.world, agent_id=1)
        self.agent2 = CoopSensAgent(name='Agent 2', world=self.world, agent_id=2)
        self.agent3 = CoopSensAgent(name='Agent 3', world=self.world, agent_id=3)


def example_1():
    env = CoopSens_Example_Environment_1()
    env.init()
    env.start(steps=10)


if __name__ == '__main__':
    example_1()