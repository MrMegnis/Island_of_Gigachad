import pygame
from base_classes.rectangle import Rectangle
from item import Item
from gui.layouts.horizontal_layout import Horizontal_Layout
from gui.layouts.vertical_layout import Vertical_Layout
from gui.widgets.button import Button


class Inventory(Rectangle):
    def __init__(self, left: int, top: int, image: str, owner, open_key=pygame.K_TAB, ) -> None:
        super(Inventory, self).__init__(left, top, image)
        size = pygame.display.get_window_size()
        self.rect.center = (size[0] // 2, size[1] // 2)
        self.items = pygame.sprite.Group()
        self.items_amount = dict()
        self.owner = owner
        self.open_key = open_key
        self.is_open = False
        self.can_interact = True
        self.item_image_left = self.rect.left + 33
        self.item_image_top = self.rect.top + 30
        self.item_icon_left = self.rect.left + 36
        self.item_icon_top = self.rect.top + 495
        self.item_icon_size = (144, 144)
        self.item_icon_space = 27
        self.items_buttons = Horizontal_Layout(self.rect.left + 36, self.rect.top + 495, self.item_icon_space)
        self.selected = None

    def set_selected(self, item):
        self.selected = item

    def clear_selected(self):
        self.selected = None

    def add_item(self, settigns_path):
        item = Item(self.item_image_left, self.item_image_top, self.item_icon_left, self.item_icon_top, self.owner,
                    settigns_path)
        if item.name not in self.items_amount.keys():
            self.items.add(item)
            self.item_icon_left += self.item_icon_size[0] + self.item_icon_space
            self.items_amount[item.name] = (item, 1)
            button = Button(0, 0, self.set_selected, self.items_amount[item.name][0], size=(144, 144), color="purple")
            self.items_buttons.add_widget(button)
        else:
            self.items_amount[item.name][1] += 1

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
            self.items_buttons.draw(screen)
            self.draw(screen)
            # pygame.draw.rect(screen, "yellow", self.items_buttons.rect)
            self.items_buttons.update()
            self.items.update(screen)
            if not isinstance(self.selected, type(None)):
                self.selected.draw(screen)
