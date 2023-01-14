import pygame
from base_classes.rectangle import Rectangle
from scripts.unpack_json import unpack_json


class Item(Rectangle):
    def __init__(self, left: int, top: int, image: str, owner, settings_path: str, stat: str = None, afix: str = None,
                 value=None) -> None:
        self.stat = stat
        self.afix = afix
        self.value = value
        self.owner = owner
        self.load_settings(settings_path)
        image = None  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        super(Item, self).__init__(left, top, image)

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

    def load_settings(self, path):
        settings = unpack_json(path)
        self.image = settings["image"]
        self.stat = settings["stat"]
        self.afix = settings["afix"]
        self.value = settings["value"]
        self.apply_afix()
