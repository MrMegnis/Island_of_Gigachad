import pygame
from gui.widgets.button import Button
from gui.layouts.vertical_layout import Vertical_Layout


class Main_Menu:
    def __init__(self, width, height, start_button_func=None, exit_button_func=None):
        self.width = width
        self.height = height
        self.background = self.image = pygame.surface.Surface((self.width, self.height))
        self.buttons_layout = Vertical_Layout(self.width // 3, self.height // 3, 100)
        self.start_button = Button(0, 0, start_button_func, "data/graphics/gui/buttons/start_button.png", color="green")
        self.exit_button = Button(0, 0, exit_button_func, "data/graphics/gui/buttons/exit_button.png", color="red")
        self.buttons_layout.add_widget(self.start_button)
        self.buttons_layout.add_widget(self.exit_button)

    def draw(self, screen):
        self.buttons_layout.draw(screen)

    def update(self, screen):
        self.buttons_layout.update()
        self.draw(screen)
