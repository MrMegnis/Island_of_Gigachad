import pygame
from base_classes.creature import Creature


class Enemy(Creature):
    def __init__(self, left: int, top: int, settings_path: str, move_speed: int = 150,
                 name: str = "aboba_warrior") -> None:
        super(Enemy, self).__init__(left, top, settings_path, move_speed=move_speed, type_="enemy", name=name)
        self.hb.lock_hb_on_owner(self.hitbox.bottomleft)

    def update(self, screen) -> None:
        super(Enemy, self).update(screen)
        self.hb.update_lock_point(self.hitbox.bottomleft)
