import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, left: int, top: int, size: int, pos: list, image: str = None, type_: int = 0, ) -> None:
        super(Player, self).__init__()
        if isinstance(image, type(None)):
            self.image = pygame.surface.Surface((size, size))
        else:
            self.image = image
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=(left + pos[0] * size, top + pos[1] * size))
        self.left = left
        self.top = top
        self.size = size
        self.pos = pos
        self.type_ = type_

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)

    def collide_with_point(self, pos) -> bool:
        return self.rect.collidepoint(pos[0], pos[1])

    def get_cords(self) -> list:
        return self.pos

    def set_image(self, image: str = None) -> None:
        if isinstance(image, type(None)):
            self.image = pygame.surface.Surface((self.size, self.size))
        else:
            self.image = image
        self.image.fill("red")

    def set_type(self, type_: int) -> None:
        self.type_ = type_
