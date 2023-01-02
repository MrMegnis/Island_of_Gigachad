import pygame


class Attack_Input:
    def __init__(self, attack=pygame.BUTTON_LEFT, alter_attack=pygame.BUTTON_RIGHT, used_buttons=None):

        if used_buttons is None:
            used_buttons = {"attack":True, "alter_attack":True}
        self.used_buttons = used_buttons
        self.attack = attack
        self.alter_attack = alter_attack

    def get_input(self) -> str:
        mouse_buttons = {pygame.BUTTON_LEFT:0, pygame.BUTTON_MIDDLE:1, pygame.BUTTON_RIGHT:2}
        mouse = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        if (keys[self.attack] or mouse[mouse_buttons[self.attack]]) and self.used_buttons["attack"]:
            return "attack"
        # elif (keys[self.alter_attack] or mouse[mouse_buttons[self.alter_attack]]) and self.used_buttons["alter_attack"]:
        #     return "alter_attack"
        return ""
