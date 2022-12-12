from copy import deepcopy
from tiles import Tile
import pygame


class Grid:
    def __init__(self, width, height, cell_size=30, left=10, top=10, border=1, grid=None):
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.border = border
        if isinstance(grid, type(None)):
            self.grid = [[Tile(self.left, self.top, self.cell_size, (j, i), "grey") for j in range(width)] for i in
                         range(height)]
        else:
            self.grid = deepcopy(grid)

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j].draw(screen)

    def get_cell(self, mouse_pos):
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j].collide_with_point(mouse_pos):
                    return (i, j)
        return None

    def on_click(self, cell_cords):
        print(cell_cords)

    def get_click(self, mouse_pos):
        cell_pos = self.get_cell(mouse_pos)
        if not isinstance(cell_pos, type(None)):
            cell = self.grid[cell_pos[0]][cell_pos[1]]
            if cell.type_ == 0:
                self.on_click(cell_pos)
