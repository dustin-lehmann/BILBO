# ======================================================================================================================
from extensions.cli.src.cli import Command, CommandSet, CommandArgument
from robots.frodo.frodo import Frodo
from utils.callbacks import Callback


# ======================================================================================================================

class FRODO_CommandSet(CommandSet):
    frodo: Frodo

    def __init__(self, frodo: Frodo):
        self.frodo = frodo
        beep_command = Command(name='beep',
                               callback=frodo.beep,
                               description='Beep the internal beeper',
                               arguments=[])

        stop_command = Command(name='stop',
                               callback=Callback(function=frodo.setSpeed,
                                                 parameters={'speed_left': 0,
                                                             'speed_right': 0}, discard_inputs=True),
                               arguments=[])

        turn_command = Command(name='turn',
                               callback=self.turn_command,
                               description='Turn the robot',
                               arguments=[
                                   CommandArgument('speed',
                                                   short_name='s',
                                                   type=float),
                                   CommandArgument('direction',
                                                   short_name='d',
                                                   type=int)

                               ])

        speed_command = Command(name='speed',
                                callback=frodo.setSpeed,
                                arguments=[
                                    CommandArgument(name='speed_left',
                                                    short_name='l',
                                                    type=float, ),
                                    CommandArgument(name='speed_right',
                                                    short_name='r',
                                                    type=float, ),
                                ])

        read_data_command = Command(name='read',
                                    callback=self.read_data,
                                    arguments=[])

        super(FRODO_CommandSet, self).__init__(name=frodo.id,
                                               commands=[beep_command,
                                                         stop_command,
                                                         speed_command,
                                                         turn_command,
                                                         read_data_command])

    # ------------------------------------------------------------------------------------------------------------------
    def turn_command(self, speed: float, direction: int):
        if direction == 1:
            self.frodo.setSpeed(speed_left=-speed, speed_right=speed)
        elif direction == -1:
            self.frodo.setSpeed(speed_left=speed, speed_right=-speed)

    # ------------------------------------------------------------------------------------------------------------------
    def read_data(self):
        data = self.frodo.getData()
        if data is not None:
            return f"{data}"
