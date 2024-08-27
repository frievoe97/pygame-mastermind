import pygame
import time

class CheckBox:
    def __init__(self, position, width, height, model, property_name, color=(232, 234, 237), checked=False):
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.color = color
        self.model = model
        self.property_name = property_name
        self.last_event_time = 0
        self.debounce_delay = 0.05  # Debounce delay in seconds

    @property
    def checked(self):
        return getattr(self.model, self.property_name)

    @checked.setter
    def checked(self, value):
        setattr(self.model, self.property_name, value)

    def draw(self, screen):
        if self.checked:
            pygame.draw.rect(screen, (255, 60, 60), self.rect.inflate(-4, -4))
        else:
            pygame.draw.rect(screen, self.color, self.rect, 2)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=E1101
            current_time = time.time()
            if current_time - self.last_event_time > self.debounce_delay:
                if self.rect.collidepoint(event.pos):
                    self.checked = not self.checked
                    self.last_event_time = current_time
