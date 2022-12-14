import pygame
from base_classes.rectangle import Rectangle


class Creature(Rectangle):
    def __init__(self, left: int, top: int, image: str = None, size: tuple = None, color="black", type_: int = 0,
                 move_speed: int = 5) -> None:
        super(Creature, self).__init__(left, top, image, size, color, type_)
        self.direction = pygame.Vector2(0, 0)
        self.move_speed = move_speed

    def move(self):
        self.rect.x += self.direction.x * self.move_speed
        self.rect.y += self.direction.y * self.move_speed
