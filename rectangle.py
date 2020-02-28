import pygame
from settings import Settings
from pygame.sprite import Sprite

# from pygame.sprite import sprite


class Rectangle(Sprite):
    """A class to create a rectangle to be at the right edge of the screen. """

    def __init__(self, ai_game):
        super().__init__()
        """ Initialize rectangle attributes. """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.color = (162, 25, 25)
        self.settings = ai_game.settings

        # Set the dimensions and properties of the rectangle.
        # this is the original code
        self.width, self.height = 200, 100
        # print(self.width)
        # self.rect = pygame.Rect(0, 0, self.width, self.height)

        # self.image = pygame.image.load("images/alien.bmp")
        # self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.image = pygame.Surface([self.width, self.height])
        # self.image = pygame.Surface(self.width, self.height)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (0, 0)

        self.rect.y = self.rect.height
        # self.rect.x = self.settings.screen_width - (self.rect.width * 2)
        self.rect.x = self.settings.screen_width - (self.rect.width * 1.2)

        self.y = float(self.rect.y)

    def draw_rectangle(self):
        """ Draw the rectangle to the screen. """
        self.screen.fill(self.color, self.rect)
        # self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_edges(self):
        """ Return True if rectangle is at the top or bottom of screen. """
        screen_rect = self.screen.get_rect()

        if self.rect.top <= 0 or self.rect.bottom >= screen_rect.bottom:
            return True

    def update(self):
        """ Move the rectangle to the top or bottom. """
        # self.y -= self.settings.alien_speed * self.settings.fleet_direction
        self.y -= self.settings.box_drop_speed * self.settings.fleet_direction
        self.rect.y = self.y
        # print(self.y)
