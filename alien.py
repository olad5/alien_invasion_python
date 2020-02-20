import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ A class to represent a single alien in the fleet. """

    def __init__(self, ai_game):
        """ Initialize the alien and set its starting position. """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        # self.rect.y = self.rect.width
        # self.rect.x = self.rect.height
        # self.rect = pygame.Rect(
        #     128, 220, self.settings.bullet_width, self.settings.bullet_height,
        # )
        self.rect.y = self.rect.height
        self.rect.x = self.settings.screen_width - (self.rect.width * 2)

        # Store the alien's exact horizontal position.
        self.y = float(self.rect.y)

    # def check_edges(self):
    #     """ Return True if alien is at the edge of screen. """
    #     screen_rect = self.screen.get_rect()

    #     if self.rect.right >= screen_rect.right or self.rect.left <= 0:
    #         return True

    # def update(self):
    #     """ Move the alien to the right. """
    #     self.y -= self.settings.alien_speed * self.settings.fleet_direction
    #     self.rect.y = self.y
    #     # print(self.y)
