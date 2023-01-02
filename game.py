import pygame
import random
from level import Level
from player import Player
from enemy import Enemy
from input_system.movement_input import Movement_Input
from scripts.unpack_column import unpack_column
from gui.layouts.vertical_layout import Vertical_Layout
from gui.layouts.horizontal_layout import Horizontal_Layout
from gui.widgets.button import Button
from gui.widgets.label import Label


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.window_width = 1000
        self.window_height = 800
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Gigachad's Island")
        self.game = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.tile_size = 50
        self.player = Player(self.tile_size * 3, self.tile_size * 3, Movement_Input(),
                             image="data/graphics/player/livesey/idle/idle.png")
        self.enemy = Enemy(self.tile_size * 3, self.tile_size * 3, image="data/graphics/enemy/aboba_warrior/idle/idle.png")
        self.button = Button(self.tile_size * 10, self.tile_size * 10, self.generate_level, color="red")
        # self.layout = Vertical_Layout(50, 50, 10)
        # self.layout = Horizontal_Layout(50, 50, 10)
        # self.layout.add_widget(Button(0, 0, color="yellow"))
        # self.layout.add_widget(Button(0, 0, color="red"))
        # self.layout.add_widget(Button(0, 0, color="yellow"))
        # self.layout.add_widget(Button(0, 0, color="red"))
        # self.layout.add_widget(Button(0, 0, color="yellow"))
        # self.layout.add_widget(Label(0, 0))
        # self.layout.add_widget(Label(0, 0))
        # self.label = Label(100, 500)
        self.scene = None
        self.generate_level()

    def run(self) -> None:
        while self.game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.screen.fill((0, 0, 0))
            self.clock.tick(self.fps)
            self.scene.update(self.screen)
            self.enemy.update()
            self.enemy.draw(self.screen)
            self.button.get_click()
            self.button.draw(self.screen)
            # self.label.draw(self.screen)
            # self.layout.update()
            # self.layout.draw(self.screen)
            pygame.display.update()
            # print([[j.size for j in i] for i in self.level.grid])

    def generate_level(self):
        level_path = "data/levels/" + random.choice(unpack_column("data/levels/levels.txt"))
        self.scene = Level(self.window_width, self.window_height, self.player, level_path)


if __name__ == "__main__":
    game = Game()
    game.run()
