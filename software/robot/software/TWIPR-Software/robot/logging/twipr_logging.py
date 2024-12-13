import dataclasses

from robot.communication.twipr_communication import TWIPR_Communication
from robot.control.twipr_control import TWIPR_Control
from robot.drive.twipr_drive import TWIPR_Drive
from robot.estimation.twipr_estimation import TWIPR_Estimation
from robot.logging.twipr_sample import TWIPR_Sample
from robot.sensors.twipr_sensors import TWIPR_Sensors


class TWIPR_Logging:

    comm: TWIPR_Communication
    control: TWIPR_Control
    sensors: TWIPR_Sensors
    estimation: TWIPR_Estimation
    drive: TWIPR_Drive
    general_sample_collect_function: callable

    sample: TWIPR_Sample
    sample_buffer: list[TWIPR_Sample]


    # === INIT =========================================================================================================
    def __init__(self, comm: TWIPR_Communication,
                 control: TWIPR_Control,
                 sensors: TWIPR_Sensors,
                 estimation: TWIPR_Estimation,
                 drive: TWIPR_Drive,
                 general_sample_collect_function: callable):

        self.comm = comm
        self.control = control
        self.sensors = sensors
        self.estimation = estimation
        self.drive = drive
        self.general_sample_collect_function = general_sample_collect_function

        # TODO: add rx stm32 callback

    # ------------------------------------------------------------------------------------------------------------------
    def init(self) -> None:
        ...

    def start(self) -> None:
        ...

    # === METHODS ======================================================================================================
    def update(self) -> None:
        sample = self.collectSample()
        sample_dict = dataclasses.asdict(sample)

        if self.comm.wifi.connected:
            self.comm.wifi.sendStream(sample_dict)

    # ------------------------------------------------------------------------------------------------------------------
    def collectSample(self) -> TWIPR_Sample:
        sample = TWIPR_Sample()

        sample.general = self.general_sample_collect_function()
        sample.control = self.control.getSample()
        sample.sensors = self.sensors.getSample()
        sample.estimation = self.estimation.getSample()
        sample.drive = self.drive.getSample()

        return sample
        #

        #
        # sample.control = self.control.getSample()
        # sample.estimation = self.estimation.getSample()
        # sample.drive = self.drive.getSample()
        # sample.sensors = self.sensors.getSample()
        #
        # sample = dataclasses.asdict(sample)
        #
        # return sample