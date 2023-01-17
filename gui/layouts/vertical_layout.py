import pygame


class Vertical_Layout(pygame.sprite.Group):
    def __init__(self, left, top, offset : int = 0, border : int = 0):
        super(Vertical_Layout, self).__init__()
        self.surface = pygame.Surface((0,0))
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
            top = last_widget.rect.top
            size = last_widget.rect.size
            widget.set_cords((self.rect.left + self.border, top + size[1] + self.offset))
            print(widget.rect.topleft)
        self.add(widget)
        width = max(self.sprites(), key=lambda x: x.rect.width).rect.width + self.border * 2
        height = sum([i.rect.height for i in self.sprites()]) + (len(self.sprites()) - 1) * self.offset + self.border * 2
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect(topleft=self.rect.topleft)