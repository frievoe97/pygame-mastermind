import pygame
import sys
sys.path.insert(0, '..')
import font_manager
class Button:
    def __init__(self, position, width, height, color=(232, 234, 237), text="", callback=None):
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.color = color
        self.text = text
        self.font = font_manager.FontManager().get_font()
        self.callback = callback
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        txt_surface = self.font.render(self.text, True, self.color)

        # Calculate padding
        text_width, text_height = self.font.size(self.text)
        padding_x = (self.rect.width - text_width) / 2 
        padding_y = (self.rect.height - text_height) / 2 

        # Blit the text surface onto the screen at the padded position
        screen.blit(txt_surface, (self.rect.x + padding_x, self.rect.y + padding_y))

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=E1101
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
