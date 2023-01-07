import pygame
from base_classes.creature import Creature
from input_system.movement_input import Movement_Input
from input_system.attack_input import Attack_Input
from weapon import Weapon


class Player(Creature):
    def __init__(self, left: int, top: int, movement_input: Movement_Input, weapon: Weapon = None, image: str = None,
                 move_speed: int = 200,
                 hp: int = 10, name: str = "livesey") -> None:
        super(Player, self).__init__(left, top, image, move_speed=move_speed, hp=hp, type_="player", name=name)
        self.movement_input = movement_input
        self.attack_input = Attack_Input()
        if isinstance(weapon, type(None)):
            self.weapon = Weapon(0, 0, (0, 0), 0, self)
        else:
            self.weapon = weapon
        self.can_attack = True
        self.can_apply_damage = True
        self.hb.resize_hb((300, 50))
        self.hb.change_cords(0, 0)

    def add_weapon(self, weapon: Weapon):
        self.weapon = weapon

    def update(self, enemies, screen) -> None:
        self.direction = self.movement_input.get_input()
        attack = self.attack_input.get_input()
        if self.can_attack:
            if attack == "attack":
                self.weapon.set_cords(self.rect.topleft)
                self.make_attack()
                self.lock_movement()
                self.can_attack = False
            elif attack == "alter_attack":
                self.can_attack = False
        if self.animator.status == "attack" and self.animator.frame_index == len(
                self.animator.animation[self.animator.status]) - 1:
            if self.can_apply_damage:
                self.weapon.hit(enemies)
            self.can_apply_damage = False
        else:
            self.can_apply_damage = True
        if self.animator.status != "attack":
            self.can_attack = True
        # self.weapon.draw_weapon_range()
        super(Player, self).update(screen)
