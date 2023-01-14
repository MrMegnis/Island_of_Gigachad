import pygame
from copy import copy


class Camera:
    def __init__(self, dx=0, dy=0):
        self.dx = dx
        self.dy = dy

    def apply(self, obj, do_automatically=False):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def move_surface(self, surface):
        rect = surface.get_rect()
        rect.x += self.dx
        rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - 1920 // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - 1080 // 2)