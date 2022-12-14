import pygame


class Rectangle(pygame.sprite.Sprite):
    def __init__(self, left: int, top: int, image: str = None, size: tuple = None, color: str = "black",
                 type_: int = 0) -> None:
        super(Rectangle, self).__init__()
        if isinstance(image, type(None)):
            if isinstance(size, type(None)):
                self.image = pygame.surface.Surface((32, 32))
            else:
                self.image = pygame.surface.Surface(size)
                self.image.fill(color)
        else:
            self.image = image
        self.rect = self.image.get_rect(topleft=(left, top))
        self.size = self.rect.size
        self.left = self.rect.left
        self.top = self.rect.top
        self.type_ = type_

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)

    def collide_with_point(self, pos) -> bool:
        return self.rect.collidepoint(pos[0], pos[1])

    def get_cords(self) -> tuple:
        return self.left, self.top

    def set_image(self, image: str = None, size: int = None, color="black") -> None:
        if isinstance(image, type(None)):
            if isinstance(size, type(None)):
                self.image = pygame.surface.Surface((64, 64))
                self.size = 64
            else:
                self.image = pygame.surface.Surface((size, size))
                self.image.fill(color)
                self.size = size
        else:
            self.image = image

    def set_type(self, type_: int) -> None:
        self.type_ = type_
