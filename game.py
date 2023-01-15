import pygame
import random
from level import Level

from scripts.unpack_column import unpack_column
from player import Player
from input_system.movement_input import Movement_Input
from main_menu import Main_Menu
from camera import Camera


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        # self.window_width = 1920
        # self.window_height = 1080
        self.window_width = 1000
        self.window_height = 700
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Gigachad's Island")
        self.game = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.tile_size = 50
        # self.player = Player(self.tile_size * 3, self.tile_size * 3, "data/characters/aboba_warrior", Movement_Input())
        # self.button = Button(self.tile_size * 10, self.tile_size * 10, self.generate_level, color="red")
        self.main_menu = Main_Menu(self.window_width, self.window_height, self.start_game, self.quit_game)
        self.scene = self.main_menu

    def return_to_main_menu(self):
        self.scene = self.main_menu

    def run(self) -> None:
        while self.game:
            # print(self.clock.get_fps())
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.return_to_main_menu()
                if event.type == pygame.QUIT:
                    self.quit_game()
            self.screen.fill("black")
            self.clock.tick(self.fps)
            self.scene.update(self.screen)

            # self.button.get_click()
            # self.button.draw(self.screen)
            pygame.display.update()

    def generate_level(self):
        level_path = "data/levels/" + random.choice(unpack_column("data/levels/levels.txt"))
        self.scene = Level(self.window_width, self.window_height, None, level_path, self.return_to_main_menu)

    def start_game(self):
        self.generate_level()

    def quit_game(self):
        pygame.quit()
        exit()


if __name__ == "__main__":
    game = Game()
    game.run()
