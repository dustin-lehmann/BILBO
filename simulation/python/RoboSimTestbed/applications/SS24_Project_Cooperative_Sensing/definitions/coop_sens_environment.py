from scioi_py_core import core
from scioi_py_core.visualization.babylon.babylon import BabylonVisualization
from applications.SS24_Project_Cooperative_Sensing.definitions.coop_sens_world import Coop_Sensing_World


class EnvironmentBase_CooperativeSensing(core.environment.Environment):
    babylon: (BabylonVisualization, None)
    world: Coop_Sensing_World
    run_mode = 'rt'
    Ts = 0.01
    name = 'environment'

    def __init__(self, visualization=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.world = Coop_Sensing_World(name='world', parent=self)

        if visualization == 'babylon':
            pass
            # self.visualization = BabylonVisualization(fetch_function=self.getVisualizationSample, *args, **kwargs)
        else:
            self.visualization = None

        # Actions
        core.scheduling.Action(name='input', object=self, priority=0, parent=self.action_step,
                               function=self.action_input)
        core.scheduling.Action(name='joystick', object=self, priority=1, parent=self.action_step,
                               function=self.action_joystick)
        core.scheduling.Action(name='logic', object=self, priority=2, parent=self.action_step,
                               function=self.action_logic)
        core.scheduling.Action(name='world', object=self, function=self.action_world, priority=3,
                               parent=self.action_step)

        core.scheduling.Action(name='visualization', object=self, priority=4, parent=self.action_step,
                               function=self.action_visualization)
        core.scheduling.Action(name='output', object=self, priority=5, parent=self.action_step,
                               function=self.action_output)

        core.scheduling.registerActions(self.world, self.scheduling.actions['world'])

    # === ACTIONS ======================================================================================================
    def _init(self, *args, **kwargs):
        ...
        # Set the world configuration in the babylon visualization if needed
        # if self.visualization is not None:
        #     self.visualization.setWorldConfig(self.world.generateWorldConfig())
        #     self.visualization.start()
        #     setBabylonSettings(status='')

    def _action_entry(self, *args, **kwargs):
        super()._action_entry(*args, **kwargs)

    def _action_step(self, *args, **kwargs):
        pass

    def action_input(self, *args, **kwargs):
        print(f"Step: {self.scheduling.tick_global} Environment - Input Phase")
        pass

    def action_logic(self, *args, **kwargs):
        print(f"Step: {self.scheduling.tick_global} Environment - Logic Phase")
        pass

    def action_joystick(self, *args, **kwargs):
        print(f"Step: {self.scheduling.tick_global} Environment - Joystick Phase")
        pass

    def action_visualization(self, *args, **kwargs):
        print(f"Step: {self.scheduling.tick_global} Environment - Visualization Phase")
        ...
        # sample = {
        #     'time': self.scheduling.tick_global * self.Ts,
        #     'world': self.world.getSample(),
        #     'settings': getBabylonSettings()
        # }
        # self.babylon.sendSample(sample)

    def action_output(self, *args, **kwargs):
        print(f"Step: {self.scheduling.tick_global} Environment - Output Phase")
        pass

    def action_world(self, *args, **kwargs):
        print(f"Step: {self.scheduling.tick_global} Environment - World Phase")
        pass
