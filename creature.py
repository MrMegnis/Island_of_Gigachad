import pygame


class Creature(pygame.sprite.Sprite):
    def __init__(self, left: int, top: int, image: str = None, size: int= None, type_: int = 0, move_speed: int = 5) -> None:
        super(Creature, self).__init__()
        if isinstance(image, type(None)):
            if isinstance(size, type(None)):
                self.image = pygame.surface.Surface((64, 64))
                self.size = 64
            else:
                self.image = pygame.surface.Surface((size, size))
                self.size = size
        else:
            self.image = image
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=(left + size, top + size))
        self.left = self.rect.left
        self.top = self.rect.top
        self.type_ = type_
        self.direction = pygame.Vector2(0, 0)
        self.move_speed = move_speed

    def move(self):
        self.rect.x += self.direction.x * self.move_speed
        self.rect.y += self.direction.y * self.move_speed

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)

    def collide_with_point(self, pos) -> bool:
        return self.rect.collidepoint(pos[0], pos[1])

    def get_cords(self) -> tuple:
        return self.rect.topleft

    def set_image(self, image: str = None) -> None:
        if isinstance(image, type(None)):
            self.image = pygame.surface.Surface((self.size, self.size))
        else:
            self.image = image
        self.image.fill("red")

    def set_type(self, type_: int) -> None:
        self.type_ = type_
