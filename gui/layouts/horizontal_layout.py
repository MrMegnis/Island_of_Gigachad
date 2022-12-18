import pygame


class Horizontal_Layout(pygame.sprite.Group):
    def __init__(self, left, top, offset : int = 0):
        super(Horizontal_Layout, self).__init__()
        self.surface = pygame.Surface((0,0))
        self.rect = self.surface.get_rect(topleft=(left, top))
        self.offset = offset

    def set_offset(self, offset):
        self.offset = offset

    def add_widget(self, widget):
        if len(self.sprites()) == 0:
            widget.set_cords(self.rect.topleft)
        else:
            last_widget = self.sprites()[-1]
            left = last_widget.rect.left
            size = last_widget.rect.size
            widget.set_cords((left + size[0] + self.offset, self.rect.top))
        self.add(widget)