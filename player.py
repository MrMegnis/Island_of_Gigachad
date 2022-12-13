import pygame
from creature import Creature
from input_system.movement_input import Movement_Input


class Player(Creature):
    def __init__(self, left: int, top: int, movement_input: Movement_Input, image: str = None, size: int = None,
                 type_: int = 0, move_speed: int = 5) -> None:
        super(Player, self).__init__(left, top, image, size, type_, move_speed)
        self.movement_input = movement_input



    def update(self) -> None:
        super(Player, self).update()
        self.direction = self.movement_input.get_input()
        self.move()
        print(self.direction)
