import pygame
import csv
from scripts.load_image import load_image


class Animator:
    def __init__(self, obj, animations: list):
        self.object = obj
        self.animation = dict()
        for i in animations:
            self.animation[i] = self.load_animation(
                f"data/graphics/{self.object.type_}/{self.object.name}/{self.object.name}_{i}/{self.object.name}_{i}_animation.csv",
                f"data/graphics/{self.object.type_}/{self.object.name}/{self.object.name}_{i}/{self.object.name}_{i}.png")
        self.status = "idle"
        self.frame_index = 0
        self.frame_duration = 500
        self.current_time = 0

    def next_frame(self):
        self.object.image = self.animation[self.status][self.frame_index][0]
        self.set_frame_duration(self.animation[self.status][self.frame_index][1])
        self.object.rect = self.object.image.get_rect(topleft=self.object.rect.topleft)
        if self.current_time > self.frame_duration * 60:
            self.current_time = 0
        self.current_time = (self.current_time + 1000)
        self.frame_index = int(
            (self.frame_index + (self.current_time / 60) // self.frame_duration) % len(self.animation[self.status]))

    def set_status(self, status):
        if self.status != status:
            self.frame_index = 0
            self.current_time = 0
        self.status = status

    def set_frame_duration(self, duration):
        self.frame_duration = duration

    def get_status(self):
        return self.status

    def load_animation(self, path: str, sheet_path: str = None):
        animation = []
        if isinstance(sheet_path, type(None)):
            with open(path) as file:
                reader = csv.reader(file, delimiter=";")
                for i in reader:
                    animation.append(
                        (load_image("/".join(path.split("/")[0:-1]) + "/" + i[0]).convert_alpha(), int(i[1])))
        else:
            sheet = load_image(sheet_path)
            with open(path) as file:
                reader = csv.DictReader(file, delimiter=";")
                for i in reader:
                    print(i)
                    frame_top_left = (int(i["left"]), int(i["top"]))
                    size = (int(i["width"]), int(i["height"]))
                    rect = pygame.Rect(frame_top_left, size)
                    animation.append((sheet.subsurface(rect), int(i["duration"])))
        return animation
