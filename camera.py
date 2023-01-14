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

    def move_surface(self, surface):
        rect = surface.get_rect()
        rect.x += self.dx
        rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.window_width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.window_height // 2)