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
        if self.afix == "add":
            self.owner.stats[self.stat] += self.value
        elif self.afix == "multiply":
            self.owner.stats[self.stat] *= self.value
        elif self.afix == "decrease":
            self.owner.stats[self.stat] -= self.value
        elif self.afix == "divide":
            self.owner.stats[self.stat] = self.owner.stats[self.stat] // self.value

    def load_settings(self, path):
        settings = unpack_json(path)
        self.image = settings["image"]
        self.stat = settings["stat"]
        self.afix = settings["afix"]
        self.value = settings["value"]
        self.apply_afix()
