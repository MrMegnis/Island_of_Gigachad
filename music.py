import pygame


class Music:
    def __init__(self):
        pygame.mixer.init()
        self.is_playing_main_theme = False

    def play_main_theme(self):
        if self.is_playing_main_theme:
            return
        pygame.mixer.music.load("music/gigachad_music.mp3")
        self.is_playing_main_theme = True
        pygame.mixer.music.play(-1)

    def play_rickroll(self):
        pygame.mixer.music.load("music/rickroll_music.mp3")
        self.is_playing_main_theme = False
        pygame.mixer.music.play(-1)

    def play_final_music(self):
        pygame.mixer.music.load("music/final_music.mp3.")
        self.is_playing_main_theme = False
        pygame.mixer.music.play(-1)
