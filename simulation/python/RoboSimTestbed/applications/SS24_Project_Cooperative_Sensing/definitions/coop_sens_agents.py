import numpy as np

from scioi_py_core import core
from applications.SS24_Project_Cooperative_Sensing.definitions.coop_sens_dynamics import Robot_Dynamics
from scioi_py_core.core.physics import PhysicalBody


class CoopSensPhysics(PhysicalBody):

    def update(self, *args, **kwargs):
        pass

    def _calcProximitySphere(self):
        pass

    def _getProximitySphereRadius(self):
        pass


class CoopSensAgent(core.agents.DynamicAgent):
    object_type = 'CoopSensAgent'
    dynamics_class = Robot_Dynamics
    space = core.spaces.Space2D()

    y: int

    def __init__(self, name: str, world, agent_id, *args, **kwargs):
        self.dynamics = self.dynamics_class()
        super().__init__(name=name, world=world, agent_id=agent_id, *args, **kwargs)

        self.physics = CoopSensPhysics()

        core.scheduling.Action(name='measuring', function=self.measuring, object=self)
        core.scheduling.Action(name='prediction', function=self.prediction, object=self)

    # ------------------------------------------------------------------------------------------------------------------

    def measuring(self):
        # here comes all the stuff happening in the measuring phase for each agent
        print(f"Step: {self.scheduling.tick_global} Agent {self.agent_id} - Measuring Phase")

        agents_in_fov = self.getAgentsinFov()

    def prediction(self):
        print(f"Step: {self.scheduling.tick_global} Agent {self.agent_id} - Prediction Phase")
        # Here comes the code for prediction
        self.prediction = self.getPrediction()

    def getAgentsinFov(self):
        other_agents = self.world.agents
        return None
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def _getParameters(self):
        ...

    def _getSample(self):
        ...

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value: (list, np.ndarray, core.spaces.State)):
        self._input = self.dynamics.input_space.map(value)
