import pygame
import csv
from scripts.load_image import load_image
from scripts.unpack_json import unpack_json


class Animator:
    def __init__(self, obj, animations: list, main_status: str = "idle_right"):
        self.object = obj
        self.animation = dict()
        self.booleans = dict()
        self.triggers = dict()
        self.can_interrupt = dict()
        for i in animations:
            self.booleans[i] = False
            self.triggers[i] = False
            self.animation[i] = self.load_animation(
                f"data/graphics/{self.object.type_}/{self.object.name}/{i}/{i}_animation.csv",
                f"data/graphics/{self.object.type_}/{self.object.name}/{i}/{i}.png")
            if "hit" not in i:
                self.can_interrupt[i] = True
            else:
                self.can_interrupt[i] = False

        self.main_status = main_status
        self.booleans[self.main_status] = True
        self.status = self.main_status
        self.frame_index = 0
        self.frame_duration = 500
        self.current_time = 0
        self.frame_change_time = pygame.time.get_ticks()
        self.funcs_on_last_frame = []

    def set_funcs_on_last_frame(self, funcs: list):
        self.funcs_on_last_frame = funcs

    def set_func_on_last_frame(self, func):
        self.funcs_on_last_frame = [func]

    def add_funcs_on_last_frame(self, funcs: list):
        self.funcs_on_last_frame += funcs

    def add_func_on_last_frame(self, func):
        self.funcs_on_last_frame += [func]

    def clear_booleans_and_triggers(self):
        for i in self.animation.keys():
            self.triggers[i] = False
            self.booleans[i] = False

    def set_bool(self, status, value):
        if (self.can_interrupt[self.status]) or not(self.booleans[self.status] or self.triggers[self.status]):
            if value:
                self.clear_booleans_and_triggers()
                self.booleans[status] = value
                self.set_status(status)
            else:
                self.booleans[status] = value

    def trigger(self, status):
        if (self.can_interrupt[self.status]) or not(self.booleans[self.status] or self.triggers[self.status]):
            self.clear_booleans_and_triggers()
            self.triggers[status] = True
            self.set_status(status)

    def return_to_main_status(self):
        self.clear_booleans_and_triggers()
        self.set_bool(self.main_status, True)

    def next_frame(self):
        time_now = pygame.time.get_ticks()
        current_frame = self.animation[self.status][self.frame_index]
        self.object.image = current_frame[0]
        self.set_frame_duration(current_frame[1])
        self.object.rect = self.object.image.get_rect(topleft=self.object.rect.topleft)
        if time_now - self.frame_change_time >= self.frame_duration:
            self.frame_index = (self.frame_index + 1)
            self.frame_change_time = time_now

        # print(self.triggers[self.status], len(self.animation[self.status]), self.status)
        if self.frame_index == len(self.animation[self.status]):
            pass
        if self.triggers[self.status] and self.frame_index == len(self.animation[self.status]):
            for func in self.funcs_on_last_frame:
                # if self.object.stats["move_speed"] == 500:
                    # print(func, self.status, self.frame_index, len(self.animation[self.status]))
                func()
            self.funcs_on_last_frame = []
            self.return_to_main_status()
        if not (self.booleans[self.status]) and not self.triggers[self.status]:
            self.return_to_main_status()
        self.frame_index = self.frame_index % len(self.animation[self.status])

    def set_main_status(self, status):
        self.main_status = status

    def set_status(self, status):
        if (self.status != status and self.can_interrupt[self.status]) or not(self.booleans[self.status] or self.triggers[self.status]):
            self.frame_index = 0
            self.current_time = 0
            self.status = status
            self.funcs_on_last_frame = []

    def set_frame_duration(self, duration):
        self.frame_duration = duration

    def get_status(self):
        return self.status

    def get_current_frame(self):
        return self.animation[self.status][self.frame_index][0]

    def load_animation(self, path: str, sheet_path: str = None, settings_path: str = None):
        animation = []
        settings = dict()
        if not isinstance(settings_path, type(None)):
            settings = unpack_json(settings_path)

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
                    if len(settings.keys()) != 0:
                        center = (int(settings["center_x"]), int(settings["center_y"]))
                    else:
                        center = (size[0] // 2, size[1] // 2)
                    animation.append((sheet.subsurface(rect), int(i["duration"]), center))
        return animation
