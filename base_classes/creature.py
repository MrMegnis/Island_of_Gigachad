import pygame
import csv
from base_classes.rectangle import Rectangle
from animator import Animator


class Creature(Rectangle):
    def __init__(self, left: int, top: int, image: str = None, size: tuple = None, move_speed: int = 5, color="black",
                 type_: str = None, name: str = None) -> None:
        super(Creature, self).__init__(left, top, image, size, color)
        self.direction = pygame.Vector2(0, 0)
        self.move_speed = move_speed
        self.name = name
        self.type_ = type_
        self.animator = Animator(self, ["idle", "move", "move_left"])

    def move(self):
        if self.direction.x == 1 and self.move_speed != 0:
            self.animator.set_status("move")
        elif self.direction.x == -1 and self.move_speed != 0:
            self.animator.set_status("move_left")
        else:
            self.animator.set_status("idle")
        self.rect.x += self.direction.x * self.move_speed
        self.rect.y += self.direction.y * self.move_speed
