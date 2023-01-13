import pygame
from base_classes.creature import Creature
from input_system.movement_input import Movement_Input
from input_system.attack_input import Attack_Input
from input_system.jump_input import Jump_Input
from inventory import Inventory
from weapon import Weapon


class Player(Creature):
    def __init__(self, left: int, top: int, settings_path : str, movement_input: Movement_Input, weapon: Weapon = None, move_speed: int = 500, hp: int = 10, name: str = "aboba_warrior") -> None:
        super(Player, self).__init__(left, top, settings_path, move_speed=move_speed, hp=hp, type_="player", name=name)
        self.movement_input = movement_input
        self.attack_input = Attack_Input()
        self.jump_input = Jump_Input()
        self.inventory = Inventory(0,0,"data/graphics/gui/inventory/inventory.png", self)
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

    def attack(self):
        self.weapon.set_cords(self.hitbox.topleft)
        self.make_attack()
        self.lock_movement()
        self.can_attack = False

    def apply_damage(self, enemies):
        if self.can_apply_damage:
            self.weapon.hit(enemies)
        self.can_apply_damage = False

    def try_attack(self, attack, enemies):
        if self.can_attack:
            if attack == "attack":
                self.attack()
                self.inventory.add_item("data/items/rom/settings.json")
            elif attack == "alter_attack":
                self.can_attack = False
                self.weapon.apply_damage([self])
        if self.animator.status == "attack" and self.animator.frame_index == len(
                self.animator.animation[self.animator.status]) - 1:
            self.apply_damage(enemies)
        else:
            self.can_apply_damage = True
        if self.animator.status != "attack":
            self.can_attack = True

    def try_jump(self, jump):
        if jump != "" and self.can_jump:
            self.jump_count = self.stats["jump_height"]
            if self.direction.x == -1:
                self.animator.trigger("jump_left")
            else:
                self.animator.trigger("jump_right")

    def update_self_damage(self):
        self.weapon.change_damage(self.stats["damage"])

    def update_direction(self):
        self.direction = self.movement_input.get_input()


    def update(self, enemies, screen) -> None:
        self.hp = self.stats["hp"]
        self.move_speed = self.stats["move_speed"]
        # self.inventory.update(screen)
        attack = self.attack_input.get_input()

        jump = self.jump_input.get_input()
        self.try_attack(attack, enemies)
        self.try_jump(jump)

        # self.weapon.draw_weapon_range()
        super(Player, self).update(screen)
