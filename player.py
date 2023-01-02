import pygame
from base_classes.creature import Creature
from input_system.movement_input import Movement_Input
from input_system.attack_input import Attack_Input

class Player(Creature):
    def __init__(self, left: int, top: int, movement_input: Movement_Input, image: str, move_speed: int = 150,
                 hp: int = 10, name: str = "aboba_warrior") -> None:
        super(Player, self).__init__(left, top, image, move_speed=move_speed, hp=hp, type_="player", name=name)
        self.movement_input = movement_input
        self.attack_input = Attack_Input()

    def update(self) -> None:
        self.direction = self.movement_input.get_input()
        attack = self.attack_input.get_input()
        if attack != "":
            self.make_attack()
            self.lock_movement()
        super(Player, self).update()
