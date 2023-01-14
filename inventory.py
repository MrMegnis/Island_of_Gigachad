import pygame
from base_classes.rectangle import Rectangle
from item import Item


class Inventory(Rectangle):
    def __init__(self, left: int, top: int, image: str, owner, open_key=pygame.K_TAB, ) -> None:
        self.items = []
        self.owner = owner
        self.open_key = open_key
        self.is_open = False
        self.can_interact = True
        super(Inventory, self).__init__(left, top, image)
        size = pygame.display.get_window_size()
        self.rect.center = (size[0] // 2, size[1] // 2)

    def add_item(self, settigns_path):
        self.items.append(Item(0, 0, "", self.owner, settigns_path))

    def interaction(self):
        keys = pygame.key.get_pressed()
        if keys[self.open_key]:
            if self.can_interact:
                self.is_open = not self.is_open
                self.can_interact = False
        else:
            self.can_interact = True

    def update(self, screen) -> None:
        self.interaction()
        if self.is_open:
            self.draw(screen)
