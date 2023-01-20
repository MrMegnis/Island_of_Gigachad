import pygame
from copy import copy


class Camera:
    def __init__(self, dx=0, dy=0):
        self.dx = dx
        self.dy = dy
        self.window_width = pygame.display.get_window_size()[0]
        self.window_height = pygame.display.get_window_size()[1]

    def apply(self, obj, do_automatically=False):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        # try:
        #     obj.hitbox.x += self.dx
        #     obj.hitbox.y += self.dy
        # except Exception as e:
        #     pass
    def apply_creature(self, obj, do_automatically=False):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        obj.hitbox.x += self.dx
        obj.hitbox.y += self.dy
        obj.weapon.rect.x += self.dx
        obj.weapon.rect.y += self.dy

    def move_surface(self, surface):
        rect = surface.get_rect()
        rect.x += self.dx
        rect.y += self.dy

    def update(self, target, level_width, level_height, surface):
        window_size = pygame.display.get_window_size()
        left = -(target.rect.x + target.rect.w // 2 - self.window_width // 2)
        top = -(target.rect.y + target.rect.h // 2 - self.window_height // 2)
        if surface.rect.x + left > 0:
            left = 0
        if surface.rect.x + left < -(level_width - window_size[0]):
            left = 0
        if surface.rect.y + top > 0 or surface.rect.y + top < -(level_height - window_size[1]):
            top = 0
        self.dx = left
        self.dy = top
