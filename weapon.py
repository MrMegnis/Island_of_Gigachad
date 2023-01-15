import pygame
from base_classes.rectangle import Rectangle


class Weapon(Rectangle):
    def __init__(self, left: int, top: int, size: tuple, damage: int, owner) -> None:
        super(Weapon, self).__init__(left, top, size=size)
        self.damage = damage
        self.owner = owner
        owner_damage = self.owner.stats["damage"]
        # self.owner.change_stat("damage", owner_damage + self.damage)

    def set_owner(self, owner):
        self.owner = owner

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def hit(self, targets):
        hited = []
        for target in targets:
            if self.rect.colliderect(target.hitbox):
                hited.append(target)
        self.apply_damage(hited)

    def change_damage(self, damage):
        self.damage = damage

    def apply_damage(self, targets):
        for target in targets:
            target.get_damage(self.owner, self.owner.stats["damage"] + self.damage)

    def draw_weapon_range(self):
        pygame.draw.rect(pygame.display.get_surface(), "yellow", self.rect)
