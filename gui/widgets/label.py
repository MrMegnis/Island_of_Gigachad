import pygame
from base_classes.rectangle import Rectangle

class Label(Rectangle):
    def __init__(self, left, top, text: str = "Text", size: int = 50, color: str = "red", background_color="black"):
        self.font = pygame.font.Font(None, size)
        image = self.font.render(text, True, color)
        super(Label, self).__init__(left, top, image, color=background_color)
