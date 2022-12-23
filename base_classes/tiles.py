import pygame
from base_classes.rectangle import Rectangle


class Tile(Rectangle):
    def __init__(self, left: int, top: int, pos: tuple, image: str = None, size: tuple = None, color: str = "black",
                 border: int = 1) -> None:
        super(Tile, self).__init__(left, top, image, size, color)
        self.border = border
        self.pos = pos
