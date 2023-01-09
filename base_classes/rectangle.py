import pygame
from scripts.load_image import load_image


class Rectangle(pygame.sprite.Sprite):
    def __init__(self, left: int, top: int, image: str = None, size: tuple = None, color: str = "black") -> None:
        super(Rectangle, self).__init__()
        if isinstance(image, type(None)):
            if isinstance(size, type(None)):
                self.image = pygame.surface.Surface((32, 32))
                self.image.fill(color)
            else:
                self.image = pygame.surface.Surface(size)
                self.image.fill(color)
        else:
            if isinstance(image, str):
                self.image = load_image(image)
            else:
                self.image = image
        self.type_ = None
        self.rect = self.image.get_rect(topleft=(left, top))
        self.size = self.rect.size
        self.left = self.rect.left
        self.top = self.rect.top

    def set_x(self, x):
        self.rect.x = x

    def set_y(self, y):
        self.rect.y = y

    def set_cords(self, cords):
        self.rect.x = cords[0]
        self.rect.y = cords[1]

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen,"red",self.rect)

    def collide_with_point(self, pos) -> bool:
        return self.rect.collidepoint(pos[0], pos[1])

    def get_cords(self) -> tuple:
        return self.left, self.top

    def set_type(self, type_: int) -> None:
        self.type_ = type_
