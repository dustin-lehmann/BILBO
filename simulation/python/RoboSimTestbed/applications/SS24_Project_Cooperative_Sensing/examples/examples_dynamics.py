from applications.SS24_Project_Cooperative_Sensing.definitions.coop_sens_dynamics import Robot_Dynamics


def example_dynamics_1():
    dyn = Robot_Dynamics()

    dyn.input = [-1, -1]

    for i in range(0, 10):
        dyn.update()
        print(dyn.state['pos'])


if __name__ == '__main__':
    example_dynamics_1()
