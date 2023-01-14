import pygame
from copy import copy
from base_classes.layer import Layer
from scripts.unpack_column import unpack_column
from scripts.unpack_csv import unpack_csv
from scripts.unpack_json import unpack_json
from enemy import Enemy
from player import Player
from input_system.movement_input import Movement_Input
from interactable_object import Intaractable_Object
from animator import Animator
from weapon import Weapon
from camera import Camera


class Level_Surface(pygame.Surface):
    def __init__(self, size, transperent: bool = False):
        if not transperent:
            super().__init__(size)
        else:
            super().__init__(size, pygame.SRCALPHA)
        self.rect = self.get_rect()


class Level:
    def __init__(self, width, height, player, path, end_of_level_func, left=0, top=0):
        # super(Level, self).__init__(width, height, path, cell_size, left, top, border)
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.player = Player(250, 100, "data/characters/aboba_warrior", Movement_Input())
        self.camera = Camera(self.player.left, self.player.top)
        # self.player.rect.bottomleft = (96, 672)
        self.player.add_weapon(
            Weapon(self.player.hitbox.left, self.player.hitbox.top,
                   (self.player.hitbox.size[0] * 4, self.player.hitbox.size[1]), 10,
                   self.player))
        self.enemies = pygame.sprite.Group()
        self.interact_objs = pygame.sprite.Group()
        self.interact_objs.add(Intaractable_Object(2592, 2496, pygame.K_e, 100, 1000, end_of_level_func,
                                                   image="data/graphics/interactavle_objects/tab.png"))

        self.enemies.add(Enemy(700, 400, "data/enemies/aboba_warrior"))

        self.layers = self.load_layers(path + "/layers.csv")

        self.prototype_obstacles = self.load_obstacles(path)
        self.obstacles = copy(self.prototype_obstacles)
        self.obstacles_surface = Level_Surface((self.width, self.height), True)
        self.draw_on_surface([self.obstacles], self.obstacles_surface)
        self.obstacles_sprite = pygame.sprite.Sprite()
        self.obstacles_sprite.image = self.obstacles_surface
        self.obstacles_sprite.rect = self.obstacles_surface.get_rect(topleft=(self.left, self.top))
        self.obstacles_sprite.mask = pygame.mask.from_surface(self.obstacles_sprite.image)


        self.player_collider = pygame.sprite.Sprite()
        surface = pygame.Surface(self.player.hitbox.size)
        surface.fill("red")
        self.player_collider.image = surface
        self.player_collider.rect = surface.get_rect()
        self.player_collider.mask = pygame.mask.from_surface(self.player_collider.image)


        self.surface = Level_Surface((self.width, self.height), True)
        self.surface_rect = self.surface.get_rect()
        self.draw_on_surface(self.layers, self.surface)

    def load_layers(self, layers_path):
        layers = []
        data = unpack_csv(layers_path, ";")
        # print(data)
        for i in data:
            layer_path = i[0]
            tiles_path = i[1]
            layer = Layer(self.width, self.height, layer_path, tiles_path, self.left, self.top)
            layers.append(layer)
            width = layer.bottomright[0]
            height = layer.bottomright[1]
            if width > self.width:
                self.width = width
            if height > self.height:
                self.height = height
        return layers

    def load_obstacles(self, path):
        obstacles_path = path + "/obstacles.txt"
        tiles_path = path + "/tiles.json"
        obstacles = Layer(self.width, self.height, obstacles_path, tiles_path, self.left, self.top)
        return obstacles

    def draw_layers(self, screen):
        for i in self.layers:
            i.draw(screen)

    def draw(self, screen):
        screen.blit(self.surface, self.surface.rect)

    def draw_on_surface(self, layers, surface):
        for i in layers:
            i.draw(surface)

    def rect_collide(self, rect, layer_group):
        r = pygame.sprite.Sprite()
        r.rect = rect
        return pygame.sprite.spritecollideany(r, layer_group)

    def rect_collide_mask(self, rect, layer_sprite):
        r = pygame.sprite.Sprite()
        surface = pygame.Surface(rect.size)
        surface.fill("red")
        r.image = surface
        r.rect = surface.get_rect(topleft=rect.topleft)
        r.mask = pygame.mask.from_surface(r.image)
        return bool(pygame.sprite.collide_mask(r, layer_sprite))

    def player_collide(self, layer):
        return pygame.sprite.spritecollideany(self.player_collider, layer)

    def player_collide_mask(self, layer_sprite):
        return not pygame.sprite.collide_mask(self.player_collider, layer_sprite)

    def player_update(self, screen):
        collide_func = self.rect_collide_mask
        obstacles = self.obstacles_sprite
        self.player.update_direction()

        if collide_func(self.player.next_move(), obstacles):
            self.player.lock_movement()
        else:
            self.player.unlock_movement()

        if self.player.jump_count != 0:
            if not collide_func(self.player.next_jump_move(), obstacles):
                self.player.do_jump()
            else:
                self.player.jump_count = 1
            self.player.jump_count -= 1

        if collide_func(self.player.next_gravity_move(), obstacles):
            for i in range(self.player.stats["gravity_strength"], -1, -1):
                if not collide_func(self.player.next_gravity_move(i), obstacles):
                    self.player.gravity_move(i)
                    # self.player.animator.return_to_main_status()
        else:
            self.player.can_attack = False
            self.player.gravity_move(self.player.stats["gravity_strength"])
            if self.player.jump_count == 0:
                if self.player.direction.x == -1:
                    self.player.animator.trigger("fall_left")
                else:
                    self.player.animator.trigger("fall_right")
            self.player.can_jump = False

        if collide_func(self.player.next_gravity_move(1), obstacles):
            if not self.player.can_jump:
                self.player.animator.return_to_main_status()
            self.player.can_jump = True
        # Вот это я насрал

        self.player.update(self.enemies.sprites(), screen)

    def camera_update(self):
        self.camera.update(self.player)
        self.camera.apply(self.surface)
        self.camera.apply(self.obstacles_sprite)
        # self.camera.apply(self.obstacles_surface)
        self.camera.apply_creature(self.player)
        # for obstacle in self.obstacles.layer:
        #     self.camera.apply(obstacle)
        for interactive_obj in self.interact_objs:
            self.camera.apply(interactive_obj)
        for enemy in self.enemies:
            self.camera.apply_creature(enemy)

    def update(self, screen):
        # self.obstacles.draw(screen)

        self.draw(screen)
        self.enemies.update(screen)
        self.player_update(screen)
        self.interact_objs.update(self.player, screen)
        self.camera_update()
