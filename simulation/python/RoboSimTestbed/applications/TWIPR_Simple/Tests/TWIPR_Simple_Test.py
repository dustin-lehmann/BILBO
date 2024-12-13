from applications.TWIPR_Simple.Environment.Environments.Environment_SingleTWIPR import Environment_SingleTWIPR, \
    Environment_SingleTWIPR_KeyboardInput
from scioi_py_core.objects.world import floor
from scioi_py_core.objects.world.grid import Grid2D
import scioi_py_core.core as core


def main():
    env = Environment_SingleTWIPR_KeyboardInput(visualization='babylon', webapp_config={'title': 'This is a title'})
    floor = Grid2D(env.world, cell_size=0.5, cells_x=10, cells_y=10, origin=[0, 0])

    env.init()
    env.start()


if __name__ == '__main__':
    main()
