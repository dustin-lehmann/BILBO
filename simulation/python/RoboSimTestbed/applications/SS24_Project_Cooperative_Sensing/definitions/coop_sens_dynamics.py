import numpy as np

from scioi_py_core import core

# Robot Spaces
Robot_InputSpace = core.spaces.Space(dimensions=[
    core.spaces.ScalarDimension(name='v'),
    core.spaces.ScalarDimension(name='psi_dot'),
])

Robot_StateSpace = core.spaces.Space2D()
Robot_OutputSpace = core.spaces.Space2D()


# Robot Dynamics
class Robot_Dynamics(core.dynamics.Dynamics):
    input_space = Robot_InputSpace
    output_space = Robot_OutputSpace
    state_space = Robot_StateSpace
    Ts = 0.01

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _dynamics(self, state: core.spaces.State, input: core.spaces.State, *args, **kwargs):
        state['pos']['x'] = state['pos']['x'] + self.Ts * input['v'] * np.cos(state['psi'].value)
        state['pos']['y'] = state['pos']['y'] + self.Ts * input['v'] * np.sin(state['psi'].value)
        state['psi'] = state['psi'] + self.Ts * input['psi_dot']

        return state

    def _output(self, state: core.spaces.State):
        output = self.output_space.getState()
        output['pos']['x'] = state['pos']['x']
        output['pos']['y'] = state['pos']['y']
        output['psi'] = state['psi']

    def _init(self, *args, **kwargs):
        pass
