import pygame


class Jump_Input:
    def __init__(self, jump=pygame.K_SPACE, used_buttons=None):
        if not used_buttons:
            used_buttons = {"jump": True}

        self.used_buttons = used_buttons
        self.jump = jump

    def get_input(self) -> str:
        keys = pygame.key.get_pressed()
        if keys[self.jump] and self.used_buttons["jump"]:
            return "jump"
        return ""
