# ======================================================================================================================
# SPACES
from scioi_py_core import core

# ======================================================================================================================
# WORLD


class Coop_Sensing_World(core.world.World):
    space = core.spaces.Space2D()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        phase_input = core.scheduling.Action(name='input', object=self, function=self.action_input, priority=9)
        phase_prediction = core.scheduling.Action(name='prediction', object=self, function=self.action_prediction,
                                               priority=10)
        phase_sensors = core.scheduling.Action(name='measuring', object=self, function=self.action_measuring, priority=11)
        phase_communication = core.scheduling.Action(name='communication', object=self,
                                                     function=self.action_communication, priority=12)
        phase_logic = core.scheduling.Action(name='update', object=self,
                                             function=self.action_update, priority=13)
        phase_logic = core.scheduling.Action(name='control', object=self,
                                             function=self.action_control, priority=14)
        phase_dynamics = core.scheduling.Action(name='dynamics', object=self,
                                                function=self.action_dynamics, priority=15)

        phase_physics_update = core.scheduling.Action(name='physics_update', object=self,
                                                      function=self.action_physics_update, priority=16)

        phase_collision = core.scheduling.Action(name='collision', object=self,
                                                 function=self.collisionCheck, priority=17)
        phase_output = core.scheduling.Action(name='output', object=self,
                                              function=self.action_output, priority=18)

    # === Actions ======================================================================================================

    def action_input(self, *args, **kwargs):
        print(f"Step: {self.scheduling.tick_global} World - Input Phase")

    def action_prediction(self, *args, **kwargs):
        print(f"Step: {self.scheduling.tick_global} World - Prediction Phase")

    def action_measuring(self, *args, **kwargs):
        print(f"Step: {self.scheduling.tick_global} World - Measuring Phase")

    def action_communication(self, *args, **kwargs):
        print(f"Step: {self.scheduling.tick_global} World - Communication Phase")

    def action_update(self, *args, **kwargs):
        print(f"Step: {self.scheduling.tick_global} World - Update Phase")

    def action_control(self, *args, **kwargs):
        print(f"Step: {self.scheduling.tick_global} World - Control Phase")

    def action_dynamics(self, *args, **kwargs):
        print(f"Step: {self.scheduling.tick_global} World - Dynamics Phase")


    def action_logic2(self, *args, **kwargs):
        pass

    def action_output(self, *args, **kwargs):
        print(f"Step: {self.scheduling.tick_global} World - Output Phase")

    def action_physics_update(self, *args, **kwargs):
        pass

    def _init(self):
        super()._init()
