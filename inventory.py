import pygame
from base_classes.rectangle import Rectangle
from item import Item


class Inventory(Rectangle):
    def __init__(self, left: int, top: int, image: str, owner) -> None:
        self.items = []
        self.owner = owner
        super(Inventory, self).__init__(left, top, image)

    def add_item(self, settigns_path):
        self.items.append(Item(0, 0, "", self.owner, settigns_path))

    def update(self, screen) -> None:
        self.draw(screen)
