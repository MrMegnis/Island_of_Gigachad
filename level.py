import pygame
from copy import deepcopy
from grid import Grid


class Level(Grid):
    def __init__(self, width, height, cell_size=30, left=10, top=10, border=1, map = None):
        super(Level, self).__init__(width, height, cell_size, left, top, border, map)
        if isinstance(map, type(None)):
            self.map = deepcopy(map)
        else:
            self.map = deepcopy(self.grid)

    def change_map(self, map):
        self.map = deepcopy(map)
