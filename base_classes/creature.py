import pygame
import csv
from base_classes.rectangle import Rectangle
from animator import Animator


class Creature(Rectangle):
    def __init__(self, left: int, top: int, image: str = None, size: tuple = None, move_speed: int = 100, hp: int = 10,
                 color="yellow", type_: str = None, name: str = None) -> None:
        super(Creature, self).__init__(left, top, image, size, color)
        self.direction = pygame.Vector2(0, 0)
        self.move_speed = move_speed
        self.name = name
        self.hp = hp
        self.can_move = True
        self.type_ = type_
        self.animator = Animator(self, ["idle", "move_right", "move_left", "attack", "hit"])

    def move(self):
        if self.direction.x == 1 and self.move_speed != 0:
            self.animator.set_bool("move_right", True)
        elif self.direction.x == -1 and self.move_speed != 0:
            self.animator.set_bool("move_left", True)
        else:
            self.animator.set_bool("move_right", False)
            self.animator.set_bool("move_left", False)
        self.left += self.direction.x * self.move_speed / 60
        self.top += self.direction.y * self.move_speed / 60
        self.rect.topleft = (self.left, self.top)

    def lock_movement(self):
        self.can_move = False

    def unlock_movement(self):
        self.can_move = True

    def next_move(self):
        left = self.left + self.direction.x * self.move_speed / 60
        top = self.top + self.direction.y * self.move_speed / 60
        rect = self.rect
        rect.topleft = (left, top)
        return rect

    def get_damage(self, damage):
        self.hp -= damage

    def get_hit(self, attacker):
        self.animator.set_status("hit")

    def make_attack(self):
        self.animator.trigger("attack")

    def update(self) -> None:
        if self.can_move:
            self.move()
        if self.animator.get_status() == "attack":
            self.lock_movement()
        else:
            self.unlock_movement()
        self.animator.next_frame()
