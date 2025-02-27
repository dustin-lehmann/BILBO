import dataclasses
from dataclasses import dataclass
from random import random
from typing import List, Dict

from robot.control.definitions import TWIPR_Control_Sample, BILBO_Control_Input
from robot.estimation.twipr_estimation import TWIPR_Estimation_Sample
from utils.dataclass_utils import freeze_dataclass_instance

from robot.logging.bilbo_sample import BILBO_Sample, BILBO_Sample_General
from utils.time import performance_analyzer


@dataclasses.dataclass
class Dataclass1:
    x: float = 1
    y: float = 2

@dataclasses.dataclass
class Dataclass2:
    a: float = 1
    b: Dataclass1 = dataclasses.field(default_factory=Dataclass1)


@performance_analyzer
def todict(data):
    return dataclasses.asdict(data)

def dataclass_test():
    sample = BILBO_Sample()


    sample2 = freeze_dataclass_instance(sample)

    d = todict(sample)
    d2 = todict(sample2)

    print(d)
    print(d2)


    # print(sample2)
    # print(sample)

if __name__ == '__main__':
    dataclass_test()
