import pygame


class Movement_Input:
    def __init__(self, key_up=pygame.K_w, key_down=pygame.K_s, key_left=pygame.K_a, key_right=pygame.K_d,
                 key_jump=pygame.K_SPACE, used_buttons=None):

        if used_buttons is None:
            used_buttons = {"key_up": True, "key_down": True, "key_left": True, "key_right": True, "key_jump": True}
        self.used_buttons = used_buttons
        self.key_up = key_up
        self.key_down = key_down
        self.key_left = key_left
        self.key_right = key_right
        self.key_jump = key_jump
        self.direction = pygame.Vector2(0, 0)

    def normalized_direction(self) -> None:
        self.direction = self.direction.normalize()

    def get_input(self) -> pygame.Vector2:
        keys = pygame.key.get_pressed()
        if keys[self.key_up] and self.used_buttons["key_up"]:
            self.direction.y = -1
        elif keys[self.key_down] and self.used_buttons["key_down"]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[self.key_left] and self.used_buttons["key_left"]:
            self.direction.x = -1
        elif keys[self.key_right] and self.used_buttons["key_right"]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        if keys[self.key_jump] and self.used_buttons["key_jump"]:
            pass
        if self.direction.x != self.direction.y != 0:
            self.normalized_direction()
        return self.direction

    def get_direction(self) -> pygame.Vector2:
        return self.direction
