import pygame

class Label:
    def __init__(self, position, text, font):
        self.position = position
        self.text = text
        self.font = font

    def draw(self, screen):
        text_surface = self.font.render(
            self.text, True, (232, 234, 237))  # Assuming white text
        screen.blit(text_surface, self.position)
