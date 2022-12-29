import pygame
from base_classes.rectangle import Rectangle


class Button(Rectangle):
    def __init__(self, left: int, top: int, func=None, image: str = None, size: tuple = None, color: str = "black"):
        super(Button, self).__init__(left, top, image, size, color)
        if isinstance(func, type(None)):
            self.func = lambda: print("click")
        else:
            self.func = func
        self.can_click = True

    def on_click(self):
        self.func()

    def get_click(self):
        pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if pressed[0] and self.collide_with_point(mouse_pos):
            if self.can_click:
                self.on_click()
                self.clicked()
        else:
            self.unclicked()

    def clicked(self):
        self.can_click = False

    def unclicked(self):
        self.can_click = True

    def update(self, *args, **kwargs) -> None:
        self.get_click()
