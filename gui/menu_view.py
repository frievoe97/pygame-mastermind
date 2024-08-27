from background_manager import BackGroundManager
import font_manager
import pygame
from config import config
from config import game_config
import numpy as np
from .commands.human_vs_human_command import HumanVsHuman

import sys
sys.path.insert(0, '..')


class MenuView:
    def __init__(self, screen, model):
        self.model = model
        self.screen = screen
        self.font = font_manager.FontManager().get_font()
        self.backgroundManager = BackGroundManager()


    def draw(self, selected_index):

        self.screen.fill((0, 0, 0))

        self.screen.blit(self.backgroundManager.background, (0, 0))

        for i, command in enumerate(self.model.menu_items):
            if game_config.COMPUTER_IS_NETWORK and isinstance(command, HumanVsHuman):
                color = (112, 120, 122)  # Gray for inactive item   
            elif i == selected_index:
                color = (255, 60, 60)  # Red for selected item
            else:
                color = (232, 234, 237)  # Dark gray for other items

            text = self.font.render(str(command), 1, color)
            text_rect = text.get_rect(center=(config.WIDTH / 2, 200 + i * 50))
            self.screen.blit(text, text_rect)

        pygame.display.flip()
