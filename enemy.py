import pygame
from base_classes.creature import Creature


class Enemy(Creature):
    def __init__(self, left: int, top: int, image: str = None, move_speed: int = 150,
                 name: str = "aboba_warrior") -> None:
        super(Enemy, self).__init__(left, top, image, move_speed=move_speed, type_="enemy", name=name)
        self.hb.lock_hb_on_owner(self.rect.bottomleft)


    def update(self, screen) -> None:
        super(Enemy, self).update(screen)
        self.hb.update_lock_point(self.rect.bottomleft)
