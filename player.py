import pygame
from base_classes.creature import Creature
from input_system.movement_input import Movement_Input
from input_system.attack_input import Attack_Input
from input_system.jump_input import Jump_Input
from inventory import Inventory
from weapon import Weapon


class Player(Creature):
    def __init__(self, left: int, top: int, settings_path: str, on_death_func, movement_input: Movement_Input, weapon: Weapon = None,
                 move_speed: int = 500, hp: int = 100, name: str = "livesey") -> None:
        super(Player, self).__init__(left, top, settings_path, on_death_func, weapon, move_speed=move_speed, hp=hp, type_="player",
                                     name=name)
        self.movement_input = movement_input
        self.attack_input = Attack_Input()
        self.jump_input = Jump_Input()
        self.inventory = Inventory(0, 0, "data/graphics/gui/inventory/inventory.png", self)
        # self.inventory.add_item("data/items/frostmourne/settings.json")
        # self.inventory.add_item("data/items/frostmourne/settings.json")
        # self.inventory.add_item("data/items/pantheon_helmet/settings.json")
        # self.inventory.add_item("data/items/pantheon_spear/settings.json")
        # self.inventory.add_item("data/items/pantheon_shield/settings.json")
        # self.inventory.add_item("data/items/rom/settings.json")
        self.hb.resize_hb((300, 50))
        self.hb.change_cords(0, 0)

    def try_attack(self, attack, enemies):
        if self.can_attack:
            if attack == "attack":
                self.attack()
                # self.inventory.add_item("data/items/rom/settings.json")
            elif attack == "alter_attack":
                self.can_attack = False
                self.weapon.apply_damage([self])
        if "attack" in self.animator.status and self.animator.frame_index == len(
                self.animator.animation[self.animator.status]) - 2:
            self.apply_damage(enemies)
        else:
            self.can_apply_damage = True
        super(Player, self).try_attack()

    def try_jump(self, jump):
        if jump != "" and self.can_jump:
            self.jump_count = self.stats["jump_height"]
            # if self.direction.x == -1:
            #     self.animator.trigger("jump_left")
            # else:
            #     self.animator.trigger("jump_right")
            self.animator.set_bool("jump_" + self.view, True)

    def draw(self, screen):
        super(Player, self).draw(screen)
        self.inventory.draw(screen)

    def update_direction(self):
        self.direction = self.movement_input.get_input()
        super(Player, self).update_direction()

    def update(self, enemies, screen) -> None:
        self.hp = self.stats["hp"]
        self.move_speed = self.stats["move_speed"]
        if "attack" not in self.animator.get_status():
            self.normalize_weapon()
        attack = self.attack_input.get_input()
        jump = self.jump_input.get_input()
        self.try_attack(attack, enemies)
        self.try_jump(jump)
        super(Player, self).update(screen)
        self.inventory.update(screen)
