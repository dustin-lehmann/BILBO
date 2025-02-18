import json
import time
import qmt

from applications.FRODO.tracker.assets import TrackedAsset, TrackedVisionRobot, vision_robot_application_assets, \
    TrackedOrigin
from applications.FRODO.tracker.tracker import Tracker
from extensions.cli.src.cli import Command, CommandSet, CommandArgument
from robots.frodo.frodo_manager import FrodoManager
from utils.logging_utils import Logger

FILE_PATH = "./applications/FRODO/experiments/input/"
POSITION_TOLERANCE = 0.10   #[m]
PSI_TOLERANCE = 0.17    #[rad]; ~10°


logger = Logger('EXPERIMENT_HANDLER')
logger.setLevel('INFO')


class FRODO_ExperimentHandler:
    manager : FrodoManager
    tracker : Tracker

    config : json
    agents : list
    movements: list

    def __init__(self, manager : FrodoManager, tracker : Tracker):
        self.manager = manager
        self.tracker = tracker
        self.agents = []

    def checkConsistency(self):
        check_passed = True

        tracked_assets = self.config['requirements']['tracked_assets']
        required_agents = self.config['requirements']['agents'].keys()
        required_statics = self.config['requirements']['statics'].keys()
        algorithm_agents = self.config['algorithm']['agents'].keys()
        algorithm_statics = self.config['algorithm']['statics'].keys()
        movement_agents = self.config['movement'].keys()
        
        for agent in required_agents:
            '''Check if required agents appear in all config parts'''
            if not agent in tracked_assets:
                logger.info(f"Found required agent {agent} that is not \
                                part of requirements::tracked_assets!")
                check_passed = False
            if not agent in algorithm_agents:
                logger.info(f"Found required agent {agent} that is not \
                                part of algorithm::agents!")
                check_passed = False
            if not agent in movement_agents:
                logger.info(f"Found required agent {agent} that is not \
                                part of movement!")
                check_passed = False
                    
            if check_passed:
                self.agents.append(agent)
        
        for static in required_statics:
            '''Check if required agents appear in all config parts'''
            if not static in tracked_assets:
                logger.info(f"Found required static {static} that is not \
                                part of requirements::tracked_assets!")
                check_passed = False
            if not static in algorithm_statics:
                logger.info(f"Found required static {static} that is not \
                                part of algorithm::statics!")
                check_passed = False

        return check_passed



    def checkRequiredPositions(self):

        if not self.tracker:
            return True

        check_passed = True
        required_assets = self.config['requirements']['tracked_assets']
        required_statics = self.config['requirements']['statics'].keys()

        for asset_str in required_assets:
            try:
                asset_type = "agents"
                if asset_str in required_statics:
                    asset_type = "statics"

                if asset_str not in self.tracker.assets:
                    logger.info(f"Required asset {asset_str} not found in Tracker!")
                    return False
                asset = self.tracker.assets[asset_str]
                asset_pos = asset.position.tolist()

                required_pos = self.config['requirements'][asset_type][asset_str]['position']
                for i in range(2):
                    delta_pos = abs(required_pos[i] - asset_pos[i])
                    if delta_pos > POSITION_TOLERANCE:
                        logger.warning(f"Required asset {asset_str} not in the right position!\n \
                                       Required: {required_pos}, found: {asset_pos}")
                        check_passed = False
                        break
                    
                if isinstance(asset, TrackedVisionRobot) and asset_type == "agents":
                    asset_psi = asset.psi

                    required_psi = self.config['requirements'][asset_type][asset_str]['psi']

                    delta_psi = abs(required_psi - asset_psi)
                    delta_psi = float(qmt.wrapToPi(delta_psi))
                    if delta_psi > PSI_TOLERANCE:
                        logger.warning(f"Required agent {asset_str} not correctly turned!\n \
                                       Required: {required_psi}, found: {asset_psi}")
                        check_passed = False
            except Exception as e:
                logger.info(f"Asset {asset_str} not correctly defined: Problem with {e}")

        return check_passed
            

    def loadMovements(self):
        '''Write movement lists to robots'''
        for agent in self.agents:
            if agent not in self.manager.robots:
                logger.warning(f"Agent {agent} not known to Frodo Manager, skipping {agent} in experiment.")
                continue

            if self.config['movement'][agent]['mode'] == 'managed':
                self.manager.robots[agent].setControlMode(3)
                for idx in range(len(self.config['movement'][agent]['movements'])):
                    time.sleep(0.1)
                    movement = self.config['movement'][agent]['movements'][str(idx)]
                    try:
                        if movement['description'] == 'wait':
                            self.manager.robots[agent].addMovement(dphi=0, radius=0, time=movement['time_s'])
                        elif movement['description'] == 'move':
                            self.manager.robots[agent].addMovement(dphi=movement['psi'], radius=movement['radius_mm'],  time=movement['time_s'])
                        else:
                            logger.info(f"Unknown movement description, skipping {movement['description']} of {agent}")
                    except Exception as e:
                        logger.info(f"Problem trying to load movement {idx} of agent {agent}: {e}\nSkipping!")
                        continue

            elif self.config['movement'][agent]['mode'] == "external":
                self.manager.robots[agent].setControlMode(2)
            else:
                self.manager.robots[agent].setControlMode(1)

    def startMovements(self):
        for agent in self.agents:
            if agent in self.manager.robots:
                self.manager.robots[agent].startNavigationMovement()


    def startExperiment(self, file_name : str):
        with open(FILE_PATH + file_name, 'r') as file:
            self.config = json.load(file)
        if self.checkConsistency() and self.checkRequiredPositions():
            self.loadMovements()
            self.startMovements()
        self.agents = []
        logger.info("Finished Experiment Setup, starting!")


class FRODO_Experiments_CLI(CommandSet):

    def __init__(self, experiment_handler: FRODO_ExperimentHandler):
        self.experiment_handler = experiment_handler
        start_experiment_command = Command(name='start', description='Start a new experiment',
                                           callback=self.start_experiment,
                                           arguments=[CommandArgument(name='file',
                                                                      short_name='f',
                                                                      type=str)],
                                                                      allow_positionals=True)

        super().__init__(name='experiments', commands=[start_experiment_command])

    def start_experiment(self, file):
        self.experiment_handler.startExperiment(file)

        return f"Start Experiment {file}"
