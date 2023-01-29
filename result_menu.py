import pygame

from gui.layouts.vertical_layout import Vertical_Layout
from gui.widgets.label import Label
from gui.widgets.button import Button


class ResultMenu:
    def __init__(self, width, height, ok_btn_func, stats):
        self.width = width
        self.height = height
        self.stats = stats
        self.background = self.image = pygame.surface.Surface((self.width, self.height))
        self.buttons_layout = Vertical_Layout(100, 100, 20)
        size = pygame.display.get_window_size()
        self.ok_button = Button(0, 0, ok_btn_func, image="data/graphics/gui/buttons/ok_button.png")
        self.enemies_label = Label(0, 0, f"Врагов убито: {self.stats['enemies_killed']}", 30)
        self.levels_label = Label(0, 0, f"Уровней пройдено: {self.stats['levels_passed']}", 30)
        self.inventory_label = Label(0, 0, f"Размер инвентаря: {self.stats['inventory_size']}", 30)
        self.buttons_layout.add_widget(self.levels_label)
        self.buttons_layout.add_widget(self.enemies_label)
        self.buttons_layout.add_widget(self.inventory_label)
        self.buttons_layout.add_widget(self.ok_button)
        self.buttons_layout.set_center((size[0] // 2, size[1] // 2))

    def draw(self, screen):
        self.buttons_layout.draw(screen)

    def update(self, screen):
        self.buttons_layout.update()
        self.draw(screen)
