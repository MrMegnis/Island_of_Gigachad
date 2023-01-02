import pygame
import csv
from scripts.load_image import load_image


class Animator:
    def __init__(self, obj, animations: list, main_status: str = "idle"):
        self.object = obj
        self.animation = dict()
        self.booleans = dict()
        self.triggers = dict()
        for i in animations:
            print(i)
            self.animation[i] = self.load_animation(
                f"data/graphics/{self.object.type_}/{self.object.name}/{i}/{i}_animation.csv",
                f"data/graphics/{self.object.type_}/{self.object.name}/{i}/{i}.png")
            self.booleans[i] = False
            self.triggers[i] = False
        self.main_status = main_status
        self.booleans[i] = True
        self.status = self.main_status
        self.frame_index = 0
        self.frame_duration = 500
        self.current_time = 0
        self.frame_change_time = pygame.time.get_ticks()
        self.loop = 0

    def set_bool(self, status, value):
        if value:
            for i in self.booleans.keys():
                self.booleans[i] = False
            self.booleans[status] = value
            self.set_status(status)
        else:
            self.booleans[status] = value

    def trigger(self, status):
        for i in self.triggers.keys():
            self.triggers[i] = False
        self.triggers[status] = True
        self.set_status(status)

    def return_to_main_status(self):
        self.set_bool(self.main_status, True)

    def next_frame(self):
        time_now = pygame.time.get_ticks()
        self.object.image = self.animation[self.status][self.frame_index][0]
        self.set_frame_duration(self.animation[self.status][self.frame_index][1])
        self.object.rect = self.object.image.get_rect(topleft=self.object.rect.topleft)
        if time_now - self.frame_change_time >= self.frame_duration:
            self.frame_index = (self.frame_index + 1)  # % len(self.animation[self.status])
            self.frame_change_time = time_now

        if self.triggers[self.status] and self.frame_index == len(self.animation[self.status]):
            self.return_to_main_status()
            self.triggers[self.status] = False
        if not (self.booleans[self.status]) and not self.triggers[self.status]:
            self.return_to_main_status()
        self.frame_index = self.frame_index % len(self.animation[self.status])

    def set_main_status(self, status):
        self.main_status = status

    def set_status(self, status):
        if self.status != status:
            self.frame_index = 0
            self.current_time = 0
        self.status = status
        self.loop = 0

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
                    frame_top_left = (int(i["left"]), int(i["top"]))
                    size = (int(i["width"]), int(i["height"]))
                    rect = pygame.Rect(frame_top_left, size)
                    animation.append((sheet.subsurface(rect), int(i["duration"])))
        return animation
