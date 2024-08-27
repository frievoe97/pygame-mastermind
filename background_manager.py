import os
import sys
import pygame
from config import config


class BackGroundManager:
    def __init__(self):
        # Finde den korrekten Pfad zur retro.png Datei
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(base_path, 'retro.png')

        self.background = pygame.image.load(image_path)
        self.background = pygame.transform.scale(self.background, (config.WIDTH, config.HEIGHT))
