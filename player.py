import pygame
from base_classes.creature import Creature
from input_system.movement_input import Movement_Input


class Player(Creature):
    def __init__(self, left: int, top: int, movement_input: Movement_Input, image: str = None, size: tuple = None,
                 color: str = "green", move_speed: int = 3, name: str = "livesey") -> None:
        super(Player, self).__init__(left, top, image, size, move_speed, color, type_="player", name=name)
        self.movement_input = movement_input

    def update(self) -> None:
        super(Player, self).update()
        self.direction = self.movement_input.get_input()
        self.move()
        self.animator.next_frame()
