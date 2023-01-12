import pygame
from base_classes.creature import Creature
from input_system.movement_input import Movement_Input
from input_system.attack_input import Attack_Input
from input_system.jump_input import Jump_Input
from weapon import Weapon


class Player(Creature):
    def __init__(self, left: int, top: int, settings_path : str, movement_input: Movement_Input, weapon: Weapon = None, move_speed: int = 500, hp: int = 10, name: str = "aboba_warrior") -> None:
        super(Player, self).__init__(left, top, settings_path, move_speed=move_speed, hp=hp, type_="player", name=name)
        self.movement_input = movement_input
        self.attack_input = Attack_Input()
        self.jump_input = Jump_Input()
        if isinstance(weapon, type(None)):
            self.weapon = Weapon(0, 0, (0, 0), 0, self)
        else:
            self.weapon = weapon
        self.can_attack = True
        self.can_jump = True
        self.can_apply_damage = True
        self.hb.resize_hb((300, 50))
        self.hb.change_cords(0, 0)

    def add_weapon(self, weapon: Weapon):
        self.weapon = weapon

    def update(self, enemies, screen) -> None:
        self.direction = self.movement_input.get_input()
        attack = self.attack_input.get_input()

        jump = self.jump_input.get_input()
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

        if jump != "" and self.can_jump:
            self.jump_count = self.stats["jump_height"]
            if self.direction.x == -1:
                self.animator.trigger("jump_left")
            else:
                self.animator.trigger("jump_right")

        # self.weapon.draw_weapon_range()
        super(Player, self).update(screen)
