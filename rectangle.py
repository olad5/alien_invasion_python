import pygame
from settings import Settings

# from pygame.sprite import sprite


class Rectangle:
    """A class to create a rectangle to be at the right edge of the screen. """

    def __init__(self, ai_game):
        """ Initialize rectangle attributes. """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.color = (162, 25, 25)
        self.settings = ai_game.settings

        # Set the dimensions and properties of the rectangle.
        self.width, self.height = 200, 100
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.rect.y = self.rect.height
        # self.rect.x = self.settings.screen_width - (self.rect.width * 2)
        self.rect.x = self.settings.screen_width - (self.rect.width * 1.2)

        self.y = float(self.rect.y)

    def draw_rectangle(self):
        """ Draw the rectangle to the screen. """
        self.screen.fill(self.color, self.rect)
        # self.screen.blit(self.msg_image, self.msg_image_rect)
