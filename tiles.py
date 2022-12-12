import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, left: int, top: int, size: int, pos: list, color: str = "black", type_: int = 0,
                 border: int = 1) -> None:
        super(Tile, self).__init__()
        self.image = pygame.surface.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(left + pos[0] * size, top + pos[1] * size))
        self.left = left
        self.top = top
        self.size = size
        self.color = color
        self.border = border
        self.pos = pos
        self.type_ = type_

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)

    def collide_with_point(self, pos) -> bool:
        return self.rect.collidepoint(pos[0], pos[1])

    def get_cords(self) -> list:
        return self.pos

    def set_color(self, color: str) -> None:
        self.color = color

    def set_type(self, type_: int) -> None:
        self.type_ = type_
