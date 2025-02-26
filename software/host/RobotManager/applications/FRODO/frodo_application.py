import math
import random
import threading
import time

from applications.FRODO.experiments.frodo_experiments import FRODO_ExperimentHandler, FRODO_Experiments_CLI
from applications.FRODO.frodo_agent import FRODO_Agent
from applications.FRODO.tracker.assets import TrackedVisionRobot, TrackedAsset
from applications.FRODO.tracker.tracker import Tracker
from extensions.cli.cli_gui import CLI_GUI_Server
from extensions.cli.src.cli import Command, CommandSet, CommandArgument
from robots.frodo.frodo import Frodo
from robots.frodo.frodo_manager import FrodoManager
from robots.frodo.utils.frodo_cli import FRODO_CommandSet
from robots.frodo.utils.frodo_manager_cli import FrodoManager_Commands
from utils.exit import ExitHandler
from utils.orientation.plot_2d.dynamic.FRODO_Web_Interface import FRODO_Web_Interface, Group
from utils.sound.sound import playSound, SoundSystem
from utils.sound.sound import speak
from utils.logging_utils import Logger, setLoggerLevel
import robots.frodo.frodo_definitions as frodo_definitions
# import utils.orientation.plot_2d.dynamic.dynamic_2d_plotter as plotter
import utils.orientation.plot_2d.dynamic.FRODO_Web_Interface as plotter
from utils.orientation.orientation_2d import rotate_vector
from utils.teleplot import sendValue
from utils.time import PrecisionTimer

setLoggerLevel('Sound', 'INFO')

time1 = time.perf_counter()


# ======================================================================================================================
class FRODO_Application:
    agents: dict[str, FRODO_Agent]
    manager: FrodoManager
    tracker: (Tracker, None)
    cli_gui: CLI_GUI_Server

    experiment_handler: FRODO_ExperimentHandler

    plotter: (FRODO_Web_Interface, None)
    logger: Logger

    _exit: bool = False
    _thread: threading.Thread

    # === CONSTRUCTOR ==================================================================================================
    def __init__(self, enable_tracking: bool = True, start_webapp=True):
        self.manager = FrodoManager()
        self.manager.callbacks.new_robot.register(self._new_robot_callback)
        self.manager.callbacks.robot_disconnected.register(self._robot_disconnected_callback)

        self.agents = {}

        if enable_tracking:
            self.tracker = Tracker()
        else:
            self.tracker = None

        if self.tracker:
            self.tracker.callbacks.new_sample.register(self._tracker_new_sample)
            self.tracker.callbacks.description_received.register(self._tracker_description_received)

        self.experiment_handler = FRODO_ExperimentHandler(self.manager, self.tracker)

        self.cli_gui = CLI_GUI_Server(address='localhost', port=8090)

        # -- IO --
        self.logger = Logger('APP')
        self.logger.setLevel('INFO')
        self.soundsystem = SoundSystem(primary_engine='etts')
        self.soundsystem.start()

        if start_webapp:
            self.plotter = FRODO_Web_Interface()
        else:
            self.plotter = None

        self._thread = threading.Thread(target=self._update_plot, daemon=True)

        # self.timer = PrecisionTimer(timeout=0.1, repeat=True, callback=self.update)

        self.exit = ExitHandler(self.close)

    # === METHODS ======================================================================================================
    def init(self):
        self.manager.init()

        if self.tracker:
            self.tracker.init()

        self._getRootCLISet()

    # ------------------------------------------------------------------------------------------------------------------
    def start(self):
        self.manager.start()
        self.cli_gui.start()
        self._thread.start()

        if self.plotter:
            self.plotter.start()
            self._prepare_plotting()

        if self.tracker:
            self.tracker.start()

        # self._thread.start()
        # self.timer.start()
        speak("Start Frodo Application")

    # ------------------------------------------------------------------------------------------------------------------
    def close(self, *args, **kwargs):
        speak("Closing Frodo Application")
        self._exit = True
        if self.plotter:
            self.plotter.close()
        time.sleep(2)

    # === METHODS ======================================================================================================
    def update(self):
        ...

    # ------------------------------------------------------------------------------------------------------------------
    def _getRootCLISet(self):

        command_set_robots = FrodoManager_Commands(self.manager)

        command_set_optitrack = CommandSet('optitrack',
                                           commands=[])

        command_set_joysticks = CommandSet('joysticks',
                                           commands=[])

        command_set_experiments = FRODO_Experiments_CLI(self.experiment_handler)

        command_set_root = CommandSet('.',
                                      child_sets=[command_set_robots,
                                                  command_set_optitrack,
                                                  command_set_joysticks,
                                                  command_set_experiments])

        self.cli_gui.updateCLI(command_set_root)

    # ------------------------------------------------------------------------------------------------------------------
    def _robot_disconnected_callback(self, robot):
        speak(f'Robot {robot.id} disconnected')
        self.cli_gui.sendLog(f'Robot {robot.id} disconnected')

        if robot.id in self.cli_gui.cli.root_set.child_sets['robots'].child_sets:
            self.cli_gui.cli.root_set.child_sets['robots'].removeChild(robot.id)
            self.cli_gui.updateCLI()

        # Remove the agent
        if robot.id in self.agents:
            del self.agents[robot.id]
            self.plotter.remove_element_by_id(f'agents/{robot.id}')

    # ------------------------------------------------------------------------------------------------------------------
    def _new_robot_callback(self, robot: Frodo):
        speak(f"New Robot {robot.id} connected")
        self.cli_gui.sendLog(f'New Robot {robot.id} connected')

        # Add a new agent
        agent = FRODO_Agent(id=robot.id, robot=robot)
        self.agents[robot.id] = agent

        if self.plotter:
            group_agents: Group = self.plotter.get_element_by_id('agents')
            group_agent = group_agents.add_group(id=robot.id)
            group_agent.add_vision_agent(id=f'{robot.id}_true',
                                         position=[0, 0],
                                         psi=0,
                                         vision_radius=1.5,
                                         vision_fov=math.radians(120),
                                         color=frodo_definitions.frodo_colors[robot.id])

        # Get the command set
        command_set_robot = FRODO_CommandSet(robot)
        self.cli_gui.cli.root_set.child_sets['robots'].addChild(command_set_robot)
        self.cli_gui.updateCLI()

    # ------------------------------------------------------------------------------------------------------------------
    def _tracker_new_sample(self, sample: dict[str, TrackedAsset]):
        optitrack_group: Group = self.plotter.get_element_by_id('optitrack')
        for id, asset in sample.items():
            if isinstance(asset, TrackedVisionRobot):

                # Update the plot
                if self.plotter:
                    optitrack_element = optitrack_group.get_element_by_id(id)
                    if optitrack_element is not None and isinstance(optitrack_element, plotter.VisionAgent):
                        optitrack_element.position = [float(asset.position[0]), float(asset.position[1])]
                        optitrack_element.psi = asset.psi

                # Update the agent
                if id in self.agents:
                    self.agents[id].updateRealState(x=asset.position[0], y=asset.position[1], psi=asset.psi)

                    # Update the real agents position in the plot
                    if self.plotter:
                        agent_element = self.plotter.get_element_by_id(f'agents/{id}/{id}_true')
                        if agent_element is not None and isinstance(agent_element, plotter.VisionAgent):
                            agent_element.position = [float(asset.position[0]), float(asset.position[1])]
                            agent_element.psi = asset.psi

    # ------------------------------------------------------------------------------------------------------------------
    def _tracker_description_received(self, assets):
        self.logger.info(f'Tracker Description Received')
        if self.plotter is not None:
            optitrack_group: Group = self.plotter.get_element_by_id('optitrack')
            for id, asset in assets.items():

                if isinstance(asset, TrackedVisionRobot):

                    if id in frodo_definitions.frodo_colors:
                        color = frodo_definitions.frodo_colors[id]
                    else:
                        color = [0.5, 0.5, 0.5]

                    optitrack_group.add_vision_agent(id=id,
                                                     position=[0, 0],
                                                     psi=0,
                                                     vision_radius=1.5,
                                                     vision_fov=math.radians(120),
                                                     color=color)

    # ------------------------------------------------------------------------------------------------------------------
    def _prepare_plotting(self):
        self.plotter.add_rectangle(id='testbed', mid=[0, 0], x=3, y=3, fill=[0.9, 0.9, 0.9])
        group_robots: Group = self.plotter.add_group(id='robots')
        self.plotter.add_group(id='optitrack')
        self.plotter.add_group(id='algorithm')
        self.plotter.add_group(id='agents')

        self.plotter.add_video("FRODO 1", "frodo1", 5000, placeholder=False)
        self.plotter.add_video("FRODO 2", "frodo2", 5000, placeholder=False)
        self.plotter.add_video("FRODO 3", "frodo3", 5000, placeholder=False)
        self.plotter.add_video("FRODO 4", "frodo4", 5000, placeholder=False)

    def _aruco_marker_plotting(self, group_element, aruco_objects_dict):
        aruco_objects_copy = aruco_objects_dict.copy()
        '''copy of aruco_objects_dict to check if a marker is still visible'''

        '''loop through all connected agents'''
        for agent in self.agents:
            agent = self.agents[agent]
            agent_element = self.plotter.get_element_by_id(f'/optitrack/{agent.id}')
            pos = agent_element.position
            psi = agent_element.psi
            data = agent.robot.getData()
            
            '''get measurement data'''
            if data is not None:
                for datum in data['sensors']['aruco_measurements']:
                    id = "marker" + str(datum['id'])
                    d_tvec = datum['translation_vec']
                    d_psi = datum['psi']
                    global_tvec = rotate_vector(d_tvec, psi)
                    global_pos = [float(pos[0] + global_tvec[0]), float(pos[1] + global_tvec[1])]
                    alt_id = "agent_" + id

                    '''check if marker was seen earlier'''
                    if not id in aruco_objects_dict:
                        '''Add aruco_marker to known markers'''
                        aruco_objects_dict[id] = {'element': None}

                        aruco_objects_dict[alt_id] = {'element': None}
                        aruco_objects_dict[alt_id]['element'] = group_element.add_agent(id=id, position=global_pos,
                                                                                    psi=d_psi, color=[1, 0, 0])
                        aruco_objects_dict[id]['element'] = group_element.add_point(id=id, x=global_pos[0],
                                                                                y=global_pos[1], color=[1, 0, 0])
                        group_element.add_line(agent.id + "to" + id, start=agent_element,
                                                end=aruco_objects_dict[id]['element'])
                    
                    else:
                        '''marker was seen earlier, set alpha to 1 to make it visible and update position'''
                        aruco_objects_dict[alt_id]['element'].alpha = 1
                        aruco_objects_dict[alt_id]['element'].position = global_pos
                        aruco_objects_dict[alt_id]['element'].psi = d_psi + psi - math.pi
                        aruco_objects_dict[id]['element'].alpha = 1
                        aruco_objects_dict[id]['element'].x = global_pos[0]
                        aruco_objects_dict[id]['element'].y = global_pos[1]
                        '''pop marker from dict copy to make clear that it has been seen'''
                        aruco_objects_copy.pop(id)

        for not_visible in aruco_objects_copy:
            '''set alpha to 0 for all markers, that were not actively seen in this iteration'''
            aruco_objects_copy[not_visible]['element'].alpha = 0


    # ------------------------------------------------------------------------------------------------------------------
    def _update_plot(self):
        group_element = self.plotter.add_group(id='aruco_objects')
        '''Aruco Object Group Element'''
        aruco_objects = {}
        '''Dictionary containing all sensed Markers'''

        while not self._exit:
            self._aruco_marker_plotting(group_element=group_element, aruco_objects_dict=aruco_objects)
            time.sleep(0.1)

    # ------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================
def start_frodo_application():
    app = FRODO_Application(enable_tracking=True, start_webapp=True)
    app.init()
    app.start()
    while True:
        time.sleep(20)


# ======================================================================================================================
if __name__ == '__main__':
    start_frodo_application()
