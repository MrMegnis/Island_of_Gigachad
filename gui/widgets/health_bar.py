import pygame


class Health_Bar:
    def __init__(self, left: int, top: int, size: tuple, owner, lock_pont: tuple = (0, 0),
                 background_color: str = "green", bar_color: str = "red"):
        self.background = pygame.surface.Surface(size)
        self.background.fill(background_color)
        self.background_rect = self.background.get_rect(topleft=(left, top))
        self.background_color = background_color
        new_size = (size[0] * 0.9, size[1] * 0.9)
        left += size[0] * 0.05
        top += size[1] * 0.05
        self.bar = pygame.surface.Surface(new_size)
        self.bar.fill(bar_color)
        self.bar_rect = self.bar.get_rect(center=self.background_rect.center)
        self.bar_color = bar_color
        self.hp = owner.hp
        self.current_hp = self.hp
        self.lock_on_owner = False
        self.lock_point = lock_pont

    def get_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp < 0:
            return
        percentage = self.current_hp / self.hp
        size = self.bar_rect.size
        new_size = (size[0] * percentage, size[1])
        self.bar = pygame.surface.Surface(new_size)
        self.bar.fill(self.bar_color)

    def draw_background(self, screen):
        screen.blit(self.background, self.background_rect)

    def draw_bar(self, screen):
        screen.blit(self.bar, self.bar_rect)

    def change_cords(self, left, top):
        self.background_rect.topleft = (left, top)
        self.bar_rect.center = self.background_rect.center

    def resize_hb(self, size: tuple):
        self.background = pygame.surface.Surface(size)
        self.background.fill(self.background_color)
        self.background_rect = self.background.get_rect(topleft=self.background_rect.topleft)
        new_size = (size[0] * 0.9, size[1] * 0.9)
        self.bar = pygame.surface.Surface(new_size)
        self.bar.fill(self.bar_color)
        self.bar_rect = self.bar.get_rect(center=self.background_rect.center)

    def update_lock_point(self, lock_point: tuple):
        self.lock_point = lock_point

    def lock_hb_on_owner(self, lock_point):
        self.lock_on_owner = True
        self.lock_point = lock_point

    def unlock_hb_from_owner(self):
        self.lock_on_owner = False

    def update(self, screen):
        self.draw_background(screen)
        self.draw_bar(screen)
        if self.lock_on_owner:
            self.background_rect.topleft = self.lock_point
            self.bar_rect.center = self.background_rect.center
