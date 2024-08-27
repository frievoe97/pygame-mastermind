""" The TextBox class is a user interface element that allows the user to input and display text"""
import pygame
import sys
sys.path.insert(0, '..')

import font_manager

class TextBox:
    """Class representing a Textbox"""

    def __init__(self, position, width, height, model, prop_name, color=(232, 234, 237)):
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.color = color
        self.model = model  # Store a reference to the model
        self.prop_name = prop_name  # The name of the property in the model
        self.font = font_manager.FontManager().get_font()
        self.active = False

    @property
    def text(self):
        """
        The `text` property returns the value of the attribute `prop_name` of the `model` object.
        :return: The `text` property is returning the value of the attribute specified by
        `self.prop_name` on the `self.model` object.
        """
        return getattr(self.model, self.prop_name)

    @text.setter
    def text(self, value):
        """
        The above function sets the value of a property in a model object.
        :param value: The value that you want to set for the text property
        """
        setattr(self.model, self.prop_name, value)

    def draw(self, screen):
        """
        The function draws a rectangle on the screen with a red border if it is active, and with the
        original color and thickness if it is not active, and also displays text inside the
        rectangle.

        :param screen: The "screen" parameter is the surface on which the drawing will be displayed. 
        It is typically the main display surface in a Pygame application
        """
        if self.active:
            # Red border with increased thickness
            pygame.draw.rect(screen, (255, 60, 60), self.rect, 4)
        else:
            # Original color and thickness
            pygame.draw.rect(screen, self.color, self.rect, 2)

        txt_surface = self.font.render(self.text, True, self.color)
        screen.blit(txt_surface, (self.rect.x+5, self.rect.y+5))

    def update(self, event):
        """
        The `update` function checks for mouse button clicks and keyboard inputs, and
        updates the `active` state and `text` variable accordingly.

        :param event: The `event` parameter is an object that represents a user input event, 
        such as a mouse click or a key press. It contains information about the type of event
        and any additional data associated with it, such as the position of a mouse click or
        the key that was pressed
        """
        if event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=E1101
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if event.type == pygame.KEYDOWN and self.active:  # pylint: disable=E1101
            if event.key == pygame.K_RETURN:  # pylint: disable=E1101
                print(self.text)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:  # pylint: disable=E1101
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
