import pygame
from config import SOUND_PATHS


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            'high': pygame.mixer.Sound(SOUND_PATHS['high']),
            'medium': pygame.mixer.Sound(SOUND_PATHS['medium'])
        }

    def play(self, alert_type):
        self.sounds[alert_type].play()

    def stop(self, alert_type):
        self.sounds[alert_type].stop()