import pygame


def load_image(path: str) -> pygame.Surface:
    image = pygame.image.load(path)
    return image
