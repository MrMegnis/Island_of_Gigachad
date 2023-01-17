import pygame


class Horizontal_Layout(pygame.sprite.Group):
    def __init__(self, left, top, offset: int = 0, border: int = 0):
        super(Horizontal_Layout, self).__init__()
        self.surface = pygame.Surface((0, 0))
        self.rect = self.surface.get_rect(topleft=(left, top))
        self.offset = offset
        self.border = border

    def set_center(self, center):
        vector = pygame.Vector2(self.rect.center) - pygame.Vector2(center)
        self.rect.center = center
        for sprite in self.sprites():
            sprite.rect.topleft -= vector

    def set_offset(self, offset):
        self.offset = offset

    def add_widget(self, widget):
        if len(self.sprites()) == 0:
            widget.set_cords((self.rect.left + self.border, self.rect.top + self.border))
            print(widget.rect.topleft)
        else:
            last_widget = self.sprites()[-1]
            left = last_widget.rect.left
            size = last_widget.rect.size
            widget.set_cords((left + size[0] + self.offset, self.rect.top + self.border))
            print(widget.rect.topleft)
        self.add(widget)
        width = sum([i.rect.width for i in self.sprites()]) + (len(self.sprites()) - 1) * self.offset + self.border * 2
        height = max(self.sprites(), key=lambda x: x.rect.height).rect.height + self.border * 2
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect(topleft=self.rect.topleft)
