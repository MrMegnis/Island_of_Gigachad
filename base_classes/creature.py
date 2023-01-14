import pygame
from base_classes.rectangle import Rectangle
from animator import Animator
from gui.widgets.health_bar import Health_Bar
from scripts.unpack_json import unpack_json
from weapon import Weapon


class Creature(Rectangle):
    def __init__(self, left: int, top: int, settings_path: str, weapon: Weapon = None, move_speed: int = 300,
                 hp: int = 50, damage: int = 10,
                 type_: str = None, name: str = None, gravity_strength: int = 10, jump_height: int = 30) -> None:
        self.base_stats = {"hp": hp, "damage": damage, "gravity_strength": gravity_strength, "move_speed": move_speed,
                           "type": type_,
                           "jump_height": jump_height}
        self.stats = self.base_stats.copy()
        # self.current_stats = self.base_stats.copy()
        self.current_hp = self.stats["hp"]
        # надо убрать все переменные-характеристики игрока
        if isinstance(weapon, type(None)):
            self.weapon = Weapon(0, 0, (0, 0), 0, self)
        else:
            self.weapon = weapon

        self.direction = pygame.Vector2(0, 0)
        self.name = name
        self.can_move = True
        self.type_ = type_
        self.animator = Animator(self, ["idle", "move_right", "move_left", "attack", "hit", "jump_right", "jump_left",
                                        "fall_right", "fall_left"])
        image = self.animator.get_current_frame()
        super(Creature, self).__init__(left, top, image)
        self.hitbox = self.rect
        self.load_settings(settings_path)
        self.jump_count = 0
        self.hb = Health_Bar(self.hitbox.left, self.hitbox.bottom, (self.hitbox.size[0], self.hitbox.size[1] // 10),
                             self)

    def change_stat(self, stat, value):
        if stat == "hp":
            self.stats[stat] = value
            self.current_hp = self.stats[stat] - (self.stats[stat] - self.current_hp)
        elif stat == "damage":
            self.stats[stat] = value
        else:
            self.stats[stat] = value

    def add_weapon(self, weapon: Weapon):
        self.weapon = weapon

    def update_weapon_damage(self):
        self.weapon.change_damage(self.stats["damage"])

    def load_settings(self, path):
        settings = unpack_json(path + "/settings.json")
        hitbox_settings = settings["hitbox"]
        width = hitbox_settings["width"]
        height = hitbox_settings["height"]
        self.hitbox = pygame.rect.Rect(self.left, self.top, width, height)
        self.rect.left = self.left - hitbox_settings["left"]
        self.rect.top = self.top - hitbox_settings["top"]

    def move(self):
        if self.animator.status != "jump_right" and self.animator.status != "jump_left" and \
                self.animator.status != "fall_left" and self.animator.status != "fall_right":
            if self.direction.x == 1 and self.stats["move_speed"] != 0:
                self.animator.set_bool("move_right", True)
            elif self.direction.x == -1 and self.stats["move_speed"] != 0:
                self.animator.set_bool("move_left", True)
            else:
                self.animator.set_bool("move_right", False)
                self.animator.set_bool("move_left", False)
        # print(int(self.direction.x), self.move_speed, int(self.direction.x) * self.move_speed / 60)
        x = int(self.direction.x * self.stats["move_speed"] / 60)
        y = int(self.direction.y * self.stats["move_speed"] / 60)
        self.rect.x += x
        self.rect.y += y
        self.hitbox.x += x
        self.hitbox.y += y
        # self.rect.topleft = (self.left, self.top)

    def lock_movement(self):
        self.can_move = False

    def unlock_movement(self):
        self.can_move = True

    def next_move(self):
        left = self.hitbox.left
        left += int(self.direction.x * self.stats["move_speed"] / 60)
        top = self.hitbox.top
        top += int(self.direction.y * self.stats["move_speed"] / 60)
        rect = self.hitbox.copy()
        rect.topleft = (left, top)
        return rect

    def next_gravity_move(self, gravity_strength=None):
        if not gravity_strength:
            gravity_strength = self.stats["gravity_strength"]
        left = self.hitbox.left
        top = self.hitbox.top
        top += gravity_strength
        rect = self.hitbox.copy()
        rect.topleft = (left, top)
        return rect

    def gravity_move(self, y):
        self.rect.y += y
        self.hitbox.y += y

    def get_damage(self, attaker, damage):
        self.current_hp -= damage
        self.hb.get_damage(damage)
        if self.current_hp <= 0:
            self.kill()
        else:
            self.get_hit(attaker)

    def get_hit(self, attacker):
        self.animator.trigger("hit")

    def make_attack(self):
        self.animator.trigger("attack")

    def do_jump(self):
        self.rect.y -= self.jump_count
        self.hitbox.y -= self.jump_count

    def next_jump_move(self):
        left = self.hitbox.left
        top = self.hitbox.top
        top -= self.jump_count - self.stats["gravity_strength"]
        rect = self.hitbox.copy()
        rect.topleft = (left, top)
        return rect

    def draw_hitbox(self):
        pygame.draw.rect(pygame.display.get_surface(), "green", self.hitbox, 5)
        pygame.draw.rect(pygame.display.get_surface(), "red", self.rect, 5)

    def update(self, screen) -> None:
        if self.can_move:
            self.move()
        if self.animator.get_status() == "attack":
            self.lock_movement()
        else:
            self.unlock_movement()
        self.animator.next_frame()
        self.hb.update(screen)
        self.draw(screen)
        self.draw_hitbox()
