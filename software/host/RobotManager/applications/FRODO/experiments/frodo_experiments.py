from extensions.cli.src.cli import Command, CommandSet, CommandArgument


class FRODO_ExperimentHandler:
    ...

    def __init__(self):
        ...

    def startExperiment(self, file: str):
        ...


class FRODO_Experiments_CLI(CommandSet):

    def __init__(self, experiment_handler: FRODO_ExperimentHandler):
        self.experiment_handler = experiment_handler
        start_experiment_command = Command(name='start', description='Start a new experiment',
                                           callback=self.start_experiment,
                                           arguments=[CommandArgument(name='file',
                                                                      short_name='f',
                                                                      type=str)])

        super().__init__(name='experiments', commands=[start_experiment_command])

    def start_experiment(self, file):
        self.experiment_handler.startExperiment(file)

        return f"Start Experiment {file}"
