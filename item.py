import pygame
from base_classes.rectangle import Rectangle
from scripts.unpack_json import unpack_json
from scripts.load_image import load_image


class Item(Rectangle):
    def __init__(self, left: int, top: int, icon_left: int, icon_top: int, owner, settings_path: str) -> None:
        self.icon_left = icon_left
        self.icon_top = icon_top
        self.name = None
        self.name_rus = None
        self.description_rus = None
        self.image_icon = None
        self.rect_icon = None
        self.stat = None
        self.afix = None
        self.value = None
        self.owner = owner
        self.load_settings(settings_path)
        super(Item, self).__init__(left, top, self.image_path)
        self.apply_afix()

    def apply_afix(self):
        for i in range(len(self.afix)):
            if self.afix[i] == "add":
                value = self.owner.stats[self.stat[i]]
                value += self.value[i]
                self.owner.change_stat(self.stat[i], value)
            elif self.afix[i] == "multiply":
                value = self.owner.stats[self.stat[i]]
                self.owner.stats[self.stat[i]] *= self.value[i]
                self.owner.change_stat(self.stat[i], value)
            elif self.afix[i] == "decrease":
                value = self.owner.stats[self.stat[i]]
                value -= self.value[i]
                self.owner.change_stat(self.stat[i], value)
            elif self.afix[i] == "divide":
                value = self.owner.stats[self.stat[i]]
                value = self.owner.stats[self.stat[i]] // self.value[i]
                self.owner.change_stat(self.stat[i], value)
            elif self.afix[i] == "add_percentage":
                value = self.owner.stats[self.stat[i]]
                value *= (1 + self.value[i] / 100)
                value = int(value)
                self.owner.change_stat(self.stat[i], value)
            elif self.afix[i] == "decrease_percentage":
                value = self.owner.stats[self.stat[i]]
                value *= (1 - self.value[i] / 100)
                value = int(value)
                self.owner.change_stat(self.stat[i], value)

    def cancel_afix(self):
        for i in range(len(self.afix)):
            if self.afix[i] == "add":
                value = self.owner.stats[self.stat[i]]
                value -= self.value[i]
                self.owner.change_stat(self.stat[i], value)
            elif self.afix[i] == "multiply":
                value = self.owner.stats[self.stat[i]]
                value = self.owner.stats[self.stat[i]] // self.value[i]
                self.owner.change_stat(self.stat[i], value)
            elif self.afix[i] == "decrease":
                value = self.owner.stats[self.stat[i]]
                value += self.value[i]
                self.owner.change_stat(self.stat[i], value)
            elif self.afix[i] == "divide":
                value = self.owner.stats[self.stat[i]]
                value *= self.value[i]
                self.owner.change_stat(self.stat[i], value)
            elif self.afix[i] == "add_percentage":
                value = self.owner.stats[self.stat[i]]
                value = value * 100 / (100 + self.value[i])
                value = int(value)
                self.owner.change_stat(self.stat[i], value)
            elif self.afix[i] == "decrease_percentage":
                value = self.owner.stats[self.stat[i]]
                value = value * 100 / (100 - self.value[i])
                value = int(value)
                self.owner.change_stat(self.stat[i], value)

    def load_settings(self, path):
        settings = unpack_json(path)
        self.name = settings["name"]
        self.name = settings["name_rus"]
        self.description = settings["description_rus"]
        self.image_path = settings["image_path"]
        self.image_icon = load_image(settings["icon_path"])
        self.rect_icon = self.image_icon.get_rect(topleft=(self.icon_left, self.icon_top))
        self.stat = settings["stat"]
        self.afix = settings["afix"]
        self.value = settings["value"]

    def draw_icon(self, screen):
        screen.blit(self.image_icon, self.rect_icon)

    def update(self, screen):
        self.draw_icon(screen)
