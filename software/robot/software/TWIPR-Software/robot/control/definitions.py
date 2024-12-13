import dataclasses
import enum


@dataclasses.dataclass
class TWIPR_Balancing_Control_Config:
    available: bool = False
    K: list = dataclasses.field(default_factory=list)  # State Feedback Gain
    u_lim: list = dataclasses.field(default_factory=list)  # Input Limits
    external_input_gain: list = dataclasses.field(
        default_factory=list)  # When using balancing control without speed control, this can scale the external input

@dataclasses.dataclass
class TWIPR_PID_Control_Config:
    Kp: float = 0
    Kd: float = 0
    Ki: float = 0
    # anti_windup: float = 0
    # integrator_saturation: float = None

@dataclasses.dataclass
class TWIPR_Speed_Control_Config:
    available: bool = False
    v: TWIPR_PID_Control_Config = dataclasses.field(default_factory=TWIPR_PID_Control_Config)
    psidot: TWIPR_PID_Control_Config = dataclasses.field(default_factory=TWIPR_PID_Control_Config)
    external_input_gain: list = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class TWIPR_Control_Config:
    name: str = ''
    description: str = ''
    balancing_control: TWIPR_Balancing_Control_Config = dataclasses.field(
        default_factory=TWIPR_Balancing_Control_Config)
    speed_control: TWIPR_Speed_Control_Config = dataclasses.field(default_factory=TWIPR_Speed_Control_Config)

class TWIPR_Control_Mode(enum.IntEnum):
    TWIPR_CONTROL_MODE_OFF = 0,
    TWIPR_CONTROL_MODE_DIRECT = 1,
    TWIPR_CONTROL_MODE_BALANCING = 2,
    TWIPR_CONTROL_MODE_VELOCITY = 3,
    # TWIPR_CONTROL_MODE_POS = 4

class TWIPR_Control_Status(enum.IntEnum):
    TWIPR_CONTROL_STATE_ERROR = 0
    TWIPR_CONTROL_STATE_NORMAL = 1
@dataclasses.dataclass
class TWIPR_ControlInput:
    @dataclasses.dataclass
    class velocity:
        forward: float = 0
        turn: float = 0
    class balancing:
        u_left: float = 0
        u_right: float = 0

    class direct:
        u_left: float = 0
        u_right: float = 0


@dataclasses.dataclass
class TWIPR_Control_Sample:
    status: TWIPR_Control_Status = dataclasses.field(
        default=TWIPR_Control_Status(TWIPR_Control_Status.TWIPR_CONTROL_STATE_ERROR))
    mode: TWIPR_Control_Mode = dataclasses.field(default=TWIPR_Control_Mode(TWIPR_Control_Mode.TWIPR_CONTROL_MODE_OFF))
    configuration: str = ''
    input: TWIPR_ControlInput = dataclasses.field(default_factory=TWIPR_ControlInput)
