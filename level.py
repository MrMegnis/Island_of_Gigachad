import pygame
from copy import deepcopy
from base_classes.layer import Layer
from scripts.unpack_column import unpack_column
from scripts.unpack_json import unpack_json


class Level:
    def __init__(self, width, height, player, path=None, left=0, top=0):
        # super(Level, self).__init__(width, height, path, cell_size, left, top, border)
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.player = player
        self.layers = self.load_layers(path)
        self.obstacles = self.load_obstacles(path)

    def load_layers(self, path):
        layers = []
        tiles_path = path+"/tiles.json"
        for layer_path in unpack_column(path + "/layers.txt"):
            layers.append(Layer(self.width, self.height, layer_path, tiles_path, self.left, self.top))
        return layers

    def load_obstacles(self, path):
        obstacles_path = path + "/obstacles.txt"
        tiles_path = path + "/tiles.json"
        obstacles = Layer(self.width, self.height, obstacles_path, tiles_path, self.left, self.top)
        return obstacles

    def draw(self, screen):
        for i in self.layers:
            i.draw(screen)

    def player_collide(self, layer):
        if layer.collide_with(self.player.rect):
            return True
        return False

    def update(self, screen):
        self.draw(screen)
        if self.obstacles.collide_with(self.player.next_move()):
            self.player.set_can_move(False)
        else:
            self.player.set_can_move(True)
        self.player.draw(screen)
        self.player.update()
