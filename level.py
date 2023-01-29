import pygame
import random
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
    def __init__(self, width, height, player, path, end_of_level_func, end_of_game_func, left=0, top=0):
        # super(Level, self).__init__(width, height, path, cell_size, left, top, border)

        # level settings
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.killed_enemies = 0
        settings = unpack_json(path+"/settings.json")

        # player setup
        player_cords = settings["start"]
        self.player = Player(player_cords[0], player_cords[1], "data/characters/aboba_warrior", end_of_game_func, Movement_Input())
        self.player.hitbox.y -= self.player.hitbox.size[1]
        self.player.rect.y -= self.player.hitbox.size[1]
        weapon = Weapon(self.player.hitbox.left, self.player.hitbox.top,
                        (self.player.hitbox.size[0] * 4, self.player.hitbox.size[1]), 10,
                        self.player)
        self.player.add_weapon(weapon)
        self.camera = Camera(self.player.left, self.player.top)
        # self.player.rect.bottomleft = (96, 672)

        # enemies setup
        # self.enemies = pygame.sprite.Group()
        # enemy = Enemy(700, 400, "data/enemies/aboba_warrior", self.enemy_death)
        # weapon_enemy = Weapon(self.player.hitbox.left, self.player.hitbox.top,
        #                       (self.player.hitbox.size[0] * 4, self.player.hitbox.size[1]), 10, enemy)
        # enemy.add_weapon(weapon_enemy)
        # self.enemies.add(enemy)
        self.enemies = self.load_enemies(path+"/enemies_settings.json")

        # interactive objects setup
        end_cords = settings["end"]
        self.interact_objs = pygame.sprite.Group()
        interact_obj = Intaractable_Object(end_cords[0], end_cords[1], pygame.K_e, 100, 1000, end_of_level_func,
                                                   image="data/graphics/interactavle_objects/tab.png")
        # interact_obj.rect.y -= interact_obj.rect.size[1]
        self.interact_objs.add(interact_obj)

        # level setup
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

        self.items_path = [
            "data/items/frostmourne/settings.json",
            "data/items/pantheon_helmet/settings.json",
            "data/items/pantheon_spear/settings.json",
            "data/items/pantheon_shield/settings.json",
            "data/items/rom/settings.json"
        ]

    def enemy_death(self):
        self.killed_enemies += 1
        item = random.choice(self.items_path)
        self.player.inventory.add_item(item)

    def create_enemy(self, left, bottom):
        self.enemies = pygame.sprite.Group()
        enemy = Enemy(left, bottom, "data/enemies/aboba_warrior", self.enemy_death)
        enemy.hitbox.y -= enemy.hitbox.size[1]
        enemy.rect.y -= enemy.hitbox.size[1]
        # enemy.hb.update(None)
        # enemy.rect.bottomleft = (left, bottom)
        # enemy.hitbox.bottomleft =
        weapon_enemy = Weapon(enemy.hitbox.left, enemy.hitbox.top, (enemy.hitbox.size[0] * 4, enemy.hitbox.size[1]), 10,
                              enemy)
        enemy.add_weapon(weapon_enemy)
        return enemy

    def load_enemies(self, enemies_settings_path):
        settings = unpack_json(enemies_settings_path)
        raw_enemies = unpack_csv(settings["enemies_map"], ";")
        space = settings["space"]
        enemies = pygame.sprite.Group()
        tile_size = settings["tile_size"]
        for row in range(len(raw_enemies)):
            # layer.append([])
            for i in range(len(raw_enemies[row])):
                if raw_enemies[row][i] != "-1":
                    enemy = self.create_enemy(i * tile_size, row * tile_size + tile_size)
                    enemies.add(enemy)
        return enemies

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
        obstacles_path = path + "/obstacles.csv"
        tiles_path = path + "/tiles.json"
        obstacles = Layer(self.width, self.height, obstacles_path, tiles_path, self.left, self.top)
        return obstacles

    def draw_layers(self, screen):
        for i in self.layers:
            i.draw(screen)

    def draw(self, screen):
        screen.blit(self.surface, self.surface.rect)
        for enemy in self.enemies.sprites():
            enemy.draw(screen)
        self.player.draw(screen)
        self.interact_objs.draw(screen)

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
            if "hit" not in self.player.animator.get_status():
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
                    self.player.update_view()
                    if self.player.animator.status != "jump_" + self.player.view:
                        self.player.animator.set_bool("jump_" + self.player.view, True)
                    # self.player.animator.return_to_main_status()
        else:
            self.player.lock_attack()
            self.player.gravity_move(self.player.stats["gravity_strength"])
            if "jump" in self.player.animator.status and "jump_" + self.player.view != self.player.animator.get_status():
                self.player.animator.set_bool("jump_" + self.player.view, True)
            # print(self.player.animator.status)
            if self.player.jump_count == 0 and "fall_" + self.player.view != self.player.animator.get_status():
                self.player.animator.set_bool("fall_" + self.player.view, True)
            self.player.can_jump = False

        if collide_func(self.player.next_gravity_move(1), obstacles):
            if not self.player.can_jump:
                self.player.animator.return_to_main_status()
            self.player.can_jump = True
            self.player.unlock_attack()
        self.player.update(self.enemies.sprites(), screen)

    def camera_update(self):
        self.camera.update(self.player, self.width, self.height, self.surface)
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
        if not self.player.inventory.is_open:
            self.camera_update()
            self.enemies.update(self.player, screen)
            self.interact_objs.update(self.player, screen)
            self.player_update(screen)
        else:
            self.player.inventory.update(screen)
        # self.obstacles.draw(screen)
        self.draw(screen)
