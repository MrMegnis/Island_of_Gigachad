import pygame
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


class Level:
    def __init__(self, width, height, player, path, end_of_level_func, left=0, top=0):
        # super(Level, self).__init__(width, height, path, cell_size, left, top, border)
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.player = Player(300, 100, "data/characters/aboba_warrior", Movement_Input())
        # self.player.rect.bottomleft = (96, 672)
        self.player.add_weapon(
            Weapon(self.player.hitbox.left, self.player.hitbox.top,
                   (self.player.hitbox.size[0] * 4, self.player.hitbox.size[1]), 10,
                   self.player))
        self.enemies = pygame.sprite.Group()
        self.interact_objs = pygame.sprite.Group()
        self.interact_objs.add(Intaractable_Object(2592, 2496, pygame.K_e, 100, 1000, end_of_level_func, image = "data/graphics/interactavle_objects/tab.png"))

        self.enemies.add(Enemy(500, 300, "data/enemies/aboba_warrior"))

        self.layers = self.load_layers(path+"/layers.csv")
        self.obstacles = self.load_obstacles(path)
        self.surface = pygame.Surface(pygame.display.get_window_size())
        self.draw_on_surface(self.surface)

    def load_layers(self, layers_path):
        layers = []
        data = unpack_csv(layers_path, ";")
        # print(data)
        for i in data:
            layer_path = i[0]
            tiles_path = i[1]
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

    def draw_on_surface(self, surface):
        for i in self.layers:
            i.draw(surface)

    def rect_collide(self, rect, layer):
        r = pygame.sprite.Sprite()
        r.rect = rect
        return pygame.sprite.spritecollideany(r, layer)

    def player_collide(self, layer):
        r = pygame.sprite.Sprite()
        r.rect = self.player.hitbox
        return pygame.sprite.spritecollideany(r, layer)
        # if layer.collide_with(self.player.hitbox):
        #     return True
        # return False

    def player_update(self, screen):
        self.player.update_direction()
        if self.rect_collide(self.player.next_move(), self.obstacles.layer):
            self.player.lock_movement()
        else:
            self.player.unlock_movement()

        if self.player.jump_count != 0:
            if not self.obstacles.collide_with(self.player.next_jump_move()):
                self.player.do_jump()
            else:
                self.player.jump_count = 1
            self.player.jump_count -= 1

        collide_gravity = self.rect_collide(self.player.next_gravity_move(), self.obstacles.layer)
        if collide_gravity:
            for i in range(self.player.stats["gravity_strength"], -1, -1):
                if not self.rect_collide(self.player.next_gravity_move(i), self.obstacles.layer):
                    self.player.gravity_move(i)
                    self.player.animator.return_to_main_status()
        else:
            self.player.gravity_move(self.player.stats["gravity_strength"])
            if self.player.jump_count == 0:
                if self.player.direction.x == -1:
                    self.player.animator.trigger("fall_left")
                else:
                    self.player.animator.trigger("fall_right")
            self.player.can_jump = False

        if self.rect_collide(self.player.next_gravity_move(1), self.obstacles.layer):
            if not self.player.can_jump:
                self.player.animator.return_to_main_status()
            self.player.can_jump = True
        # Вот это я насрал

        self.player.update(self.enemies.sprites(), screen)

    def update(self, screen):
        # self.draw(screen)
        screen.blit(self.surface, self.surface.get_rect(topleft=(0,0)))
        # self.obstacles.draw(screen)
        self.enemies.update(screen)
        self.player_update(screen)
        self.interact_objs.update(self.player, screen)
