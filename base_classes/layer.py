from copy import deepcopy

import pygame

from base_classes.tiles import Tile
from scripts.unpack_layer import unpack_layer
from scripts.unpack_json import unpack_json


class Layer:
    def __init__(self, width, height, layer_path: str, tile_path: str, left=0,top=0):
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.tile_size = 0
        self.layer = self.load_layer(layer_path, tile_path)

    def load_layer(self, layer_path, tiles_path, return_type: str = "surface"):
        raw_layer = unpack_layer(layer_path)
        tiles_data = unpack_json(tiles_path)
        self.tile_size = tiles_data["tile_size"]
        layer = []
        for row in range(len(raw_layer)):
            layer.append([])
            for i in range(len(raw_layer[row])):
                tile_image = tiles_data[raw_layer[row][i]]
                if tile_image != "":
                    layer[-1].append(Tile(self.left + self.tile_size * i, self.top + self.tile_size * row, tile_image))
        return layer

    def collide_with(self, rect):
        for i in self.layer:
            for j in i:
                if rect.colliderect(j.rect):
                    return True
        return False

    def draw(self, screen):
        for row in self.layer:
            for tile in row:
                tile.draw(screen)