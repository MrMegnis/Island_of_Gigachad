from copy import deepcopy

import pygame

from base_classes.tiles import Tile
from scripts.unpack_layer import unpack_layer
from scripts.unpack_csv import unpack_csv
from scripts.unpack_json import unpack_json


class Layer:
    def __init__(self, width, height, layer_path: str, tile_path: str, left=0, top=0):
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.tile_size = 0
        self.bottomright = (0, 0)
        self.layer = self.load_layer(layer_path, tile_path)

    def load_layer(self, layer_path, tiles_path, return_type: str = "surface") -> pygame.sprite.Group:
        # print(layer_path, tiles_path)
        if layer_path.split(".")[-1] != "csv":
            raw_layer = unpack_layer(layer_path)
        else:
            raw_layer = unpack_csv(layer_path, ";")
        # print(raw_layer)
        tiles_data = unpack_json(tiles_path)
        self.tile_size = tiles_data["tile_size"]
        layer = pygame.sprite.Group()
        for row in range(len(raw_layer)):
            # layer.append([])
            for i in range(len(raw_layer[row])):
                tile_image = tiles_data[raw_layer[row][i]]
                if tile_image != "":
                    tile = Tile(self.left + self.tile_size * i, self.top + self.tile_size * row, tile_image)
                    layer.add(tile)
                    if tile.rect.bottomright > self.bottomright:
                        self.bottomright = tile.rect.bottomright
        return layer

    def collide_with(self, rect):
        for i in self.layer:
            if rect.colliderect(i.rect):
                return True
        return False

    def apply_offset(self, camera, screen):
        for sprite in self.layer:
            camera.apply(sprite)
            screen.blit(sprite.image, sprite.rect)

    def draw(self, screen):
        self.layer.draw(screen)
