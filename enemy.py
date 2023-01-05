import pygame
from base_classes.creature import Creature


class Enemy(Creature):
    def __init__(self, left: int, top: int, image: str = None, move_speed: int = 150,
                 name: str = "aboba_warrior") -> None:
        super(Enemy, self).__init__(left, top, image, move_speed=move_speed, type_="enemy", name=name)
        # self.set_can_move(False)

    def update(self) -> None:
        super(Enemy, self).update()
