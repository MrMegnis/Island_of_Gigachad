import pygame
import csv


class Animator:
    def __init__(self, obj, animations: list):
        self.object = obj
        self.animation = dict()
        for i in animations:
            self.animation[i] = self.load_animation(
                f"data/graphics/{self.object.type_}/{self.object.name}/{self.object.name}_{i}/{self.object.name}_{i}_animation.csv")
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
        print(self.current_time / 60, self.frame_index)

    def set_status(self, status):
        if self.status != status:
            self.frame_index = 0
            self.current_time = 0
        self.status = status

    def set_frame_duration(self, duriation):
        self.frame_duration = duriation

    def get_status(self):
        return self.status

    def load_animation(self, path):
        animation = []
        with open(path) as file:
            reader = csv.reader(file, delimiter=";")
            for i in reader:
                animation.append(
                    (pygame.image.load("/".join(path.split("/")[0:-1]) + "/" + i[0]).convert_alpha(), int(i[1])))
        return animation
