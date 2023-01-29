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
        self.name_font = pygame.font.Font(None, 50)
        self.name_left = self.rect.left + 303
        self.name_top = self.rect.top + 3
        self.name_color = (227, 159, 0)
        self.description_font = pygame.font.Font(None, 40)
        self.description_left = self.rect.left + 303
        self.description_top = self.rect.top + 90
        self.description_space = 30
        self.description_string_max_len = 500
        self.description_color = (227, 159, 0)
        self.item_image_left = self.rect.left + 33
        self.item_image_top = self.rect.top + 30
        self.item_icon_left = self.rect.left + 36
        self.item_icon_top = self.rect.top + 495
        self.item_icon_size = (144, 144)
        self.item_icon_space = 27
        self.items_buttons = Horizontal_Layout(self.rect.left + 36, self.rect.top + 495, self.item_icon_space)
        self.selected = None

        self.drop_button = Button(self.left, self.top, self.decrease_selected_amount,
                                  image="data/graphics/gui/buttons/drop_button.png")
        self.drop_button.rect.center = (self.rect.left + 150, self.rect.top + 375)

    def add_item(self, settigns_path):
        item = Item(self.item_image_left, self.item_image_top, self.item_icon_left, self.item_icon_top, self.owner,
                    settigns_path)
        if item.name not in self.items_amount.keys():
            self.items.add(item)
            self.item_icon_left += self.item_icon_size[0] + self.item_icon_space
            self.items_amount[item.name] = [item, 1]
            button = Button(0, 0, self.set_selected, [self.items_amount[item.name][0]], size=(144, 144), color="purple")
            self.items_buttons.add_widget(button)
        else:
            self.items_amount[item.name][1] += 1


    def get_inventory_size(self):
        print(self.items, self.items_amount)
        return len(self.items_amount)

    def decrease_selected_amount(self):
        if not isinstance(self.selected, type(None)) and self.items_amount[self.selected.name][1] > 1:
            self.items_amount[self.selected.name][1] -= 1
            self.selected.cancel_afix()

    def interaction(self):
        keys = pygame.key.get_pressed()
        if keys[self.open_key]:
            if self.can_interact:
                self.is_open = not self.is_open
                self.can_interact = False
        else:
            self.can_interact = True

    def set_selected(self, item):
        self.selected = item

    def clear_selected(self):
        self.selected = None

    def draw_selected(self, screen):
        if not isinstance(self.selected, type(None)):
            self.selected.draw(screen)
            name_text = self.name_font.render(self.selected.name, True, self.name_color)
            screen.blit(name_text, (self.name_left, self.name_top))
            # print(self.description_font.size(self.selected.description_rus), len(self.selected.description_rus))
            if self.description_font.size(self.selected.description)[0] > self.description_string_max_len:
                size = self.description_font.size(self.selected.description)[0] // len(self.selected.description)
                strings = []
                string = ""
                for i in self.selected.description.split(" "):
                    if "\n" in i:
                        pref, suf = i.split()
                        string += pref
                        strings.append(string)
                        string = suf + " "
                    elif len(string + i + " ") * size >= self.description_string_max_len:
                        strings.append(string)
                        string = i + " "
                    else:
                        string += i + " "
                strings.append(string)
                strings.append("Количество: " + str(self.items_amount[self.selected.name][1]))
            else:
                strings = [self.selected.description_rus]
            for index, string in enumerate(strings):
                description_text = self.description_font.render(string, True, self.description_color)
                screen.blit(description_text,
                            (self.description_left, self.description_top + self.description_space * index))

    def draw(self, screen) -> None:
        if self.is_open:
            super(Inventory, self).draw(screen)
            # self.items_buttons.draw(screen)
            self.items.update(screen)
            self.draw_selected(screen)
            self.drop_button.draw(screen)

    def update(self, screen) -> None:
        self.interaction()
        if self.is_open:
            # self.draw(screen)
            # pygame.draw.rect(screen, "yellow", self.items_buttons.rect)
            self.items_buttons.update()
            self.drop_button.update()
            # self.items.update(screen)
            # self.draw_selected(screen)
