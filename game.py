import pygame, sys
from level import Level
from player import Player
from input_system.movement_input import Movement_Input
from Vector import Vector


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.window_width = 1000
        self.window_height = 800
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Game")
        self.game = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.tile_size = 50
        print(dir(Player))
        self.player = Player(100, 100, Movement_Input(), size=self.tile_size)
        self.level = Level(self.window_width // self.tile_size + 1, self.window_height // self.tile_size + 1, self.player, self.tile_size, 0, 0)

    def run(self) -> None:
        while self.game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.screen.fill((0, 0, 0))
            self.clock.tick(self.fps)
            self.level.render(self.screen)
            self.level.update(self.screen)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
