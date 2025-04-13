# a fphenix Wheel of Fortune Game
from os.path import dirname, realpath

CWD = dirname(realpath(__file__))

from gameobj.manager import Manager

if __name__ == '__main__':
    manager = Manager(CWD)
    manager.run()