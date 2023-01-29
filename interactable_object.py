import pygame
from base_classes.rectangle import Rectangle


class Intaractable_Object(Rectangle):
    def __init__(self, left: int, top: int, interact_button, interact_distance, interact_interval, interact_func, image: str = None, size: tuple = None, color: str = "black"):
        super(Intaractable_Object, self).__init__(left, top, image, size, color)
        self.interact_button = interact_button
        self.interact_func = interact_func
        self.interact_distance = interact_distance
        self.interact_interval = interact_interval
        self.interact_time = -1

    def try_interact(self, player):
        cur_time = pygame.time.get_ticks()
        if cur_time - self.interact_time >= self.interact_interval:
            if abs(self.rect.center[0] - player.rect.center[0]) <= self.interact_distance:
                    if pygame.key.get_pressed()[self.interact_button]:
                        self.interact_func()
                        self.interact_time = cur_time

    def update(self, player, screen) -> None:
        self.try_interact(player)
        # self.draw(screen)
