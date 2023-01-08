import pygame
from base_classes.layer import Layer
from scripts.unpack_column import unpack_column
from scripts.unpack_json import unpack_json
from enemy import Enemy
from player import Player
from input_system.movement_input import Movement_Input
from interactable_object import Intaractable_Object


class Level:
    def __init__(self, width, height, player, path, end_of_level_func, left=0, top=0):
        # super(Level, self).__init__(width, height, path, cell_size, left, top, border)
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.player = self.player = Player(100, 250, Movement_Input())
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Enemy(500, 250))
        self.interact_objs = pygame.sprite.Group()
        self.interact_objs.add(Intaractable_Object(800, 300, pygame.K_e, 100, 1000, end_of_level_func, image = "data/graphics/interactavle_objects/tab.png"))
        self.layers = self.load_layers(path)
        self.obstacles = self.load_obstacles(path)

    def load_layers(self, path):
        layers = []
        tiles_path = path + "/tiles.json"
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
        self.enemies.update(screen)
        self.enemies.draw(screen)
        self.interact_objs.update(self.player, screen)
        if self.obstacles.collide_with(self.player.next_move()):
            self.player.lock_movement()
        else:
            self.player.unlock_movement()
        self.player.update(self.enemies.sprites(), screen)
        self.player.draw(screen)
