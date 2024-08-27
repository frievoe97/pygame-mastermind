import sys
from typing import TYPE_CHECKING
import pygame
from config import config

if TYPE_CHECKING:
    from .menu_model import MenuModel
    from .menu_view import MenuView

class MenuController:
    def __init__(self, model: 'MenuModel', view: 'MenuView'):
        self.model = model
        self.view = view
        self.selected_index = 0

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos_x, pos_y = pygame.mouse.get_pos()
            for i, command in enumerate(self.model.menu_items):
                text = self.view.font.render(str(command), 1, (255, 255, 255))
                text_rect = text.get_rect(center=(config.WIDTH / 2, 200 + i * 50))
                if text_rect.collidepoint(pos_x, pos_y):
                    self.selected_index = i
                    command.execute()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.model.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.model.menu_items)
            elif event.key == pygame.K_RETURN:
                self.model.menu_items[self.selected_index].execute()

        # Draw the view after handling the event
        self.view.draw(self.selected_index)
