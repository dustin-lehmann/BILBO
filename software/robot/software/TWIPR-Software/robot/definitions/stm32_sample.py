import ctypes

# Samples LL
SAMPLE_BUFFER_SIZE = 10

class sample_general(ctypes.Structure):
    _fields_ = [("tick", ctypes.c_uint32),
                ("status", ctypes.c_int8),
                ("error", ctypes.c_uint8)]


class twipr_gyr_data(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float),
                ("z", ctypes.c_float)]


class twipr_acc_data(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float),
                ("z", ctypes.c_float)]


class twipr_sensor_data(ctypes.Structure):
    _fields_ = [("speed_left", ctypes.c_float),
                ("speed_right", ctypes.c_float),
                ("acc", twipr_acc_data),
                ("gyr", twipr_gyr_data),
                ("battery_voltage", ctypes.c_float)]


class twipr_estimation_state(ctypes.Structure):
    _fields_ = [("v", ctypes.c_float),
                ("theta", ctypes.c_float),
                ("theta_dot", ctypes.c_float),
                ("psi", ctypes.c_float),
                ("psi_dot", ctypes.c_float)]


class sample_estimation(ctypes.Structure):
    _fields_ = [('state', twipr_estimation_state)]


class twipr_control_external_input(ctypes.Structure):
    _fields_ = [("u_direct_1", ctypes.c_float),
                ("u_direct_2", ctypes.c_float),
                ("u_balancing_1", ctypes.c_float),
                ("u_balancing_2", ctypes.c_float),
                ("u_velocity_forward", ctypes.c_float),
                ("u_velocity_turn", ctypes.c_float),
                ]


class twipr_control_data(ctypes.Structure):
    _fields_ = [("input_velocity_forward", ctypes.c_float),
                ("input_velocity_turn", ctypes.c_float),
                ("input_balancing_1", ctypes.c_float),
                ("input_balancing_2", ctypes.c_float),
                ("input_left", ctypes.c_float),
                ("input_right", ctypes.c_float),
                ("output_left", ctypes.c_float),
                ("output_right", ctypes.c_float),
                ]


class sample_control(ctypes.Structure):
    _fields_ = [('status', ctypes.c_int8),
                ('mode', ctypes.c_int8),
                ("external_input", twipr_control_external_input),
                ("data", twipr_control_data),
                ]


class sample_sequence(ctypes.Structure):
    _fields_ = [("sequence_id", ctypes.c_uint16),
                ("sequence_tick", ctypes.c_uint32)
                ]


class twipr_stm32_sample(ctypes.Structure):
    _fields_ = [("general", sample_general),
                ("control", sample_control),
                ("estimation", sample_estimation),
                ("sensors", twipr_sensor_data),
                ("sequence", sample_sequence)]


# class trajectory_input(ctypes.Structure):
#     _fields_ = [("step", ctypes.c_uint32),
#                 ("u_1", ctypes.c_float),
#                 ("u_2", ctypes.c_float)]
#
#
# class trajectory_struct(ctypes.Structure):
#     _fields_ = [('step', ctypes.c_uint16),
#                 ('id', ctypes.c_uint16),
#                 ('length', ctypes.c_uint16)]
