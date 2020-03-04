import pygame.font
from pygame.sprite import Sprite


class Button(Sprite):
    def __init__(self, ai_game, msg):
        """ Initialize button attributes. """
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # The button message needs to be prepped only once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """ Turn msg into a renedered image and center text on the button. """
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        # self.msg_image_rect.center = self.rect.center

    def easy_button(self):
        """ This is the easy button. """
        self.rect = pygame.Rect(200, 370, self.width, self.height)
        self.msg_image_rect.center = self.rect.center
        self.draw_button()

    def medium_button(self):
        """ This is the medium button. """
        self.rect = pygame.Rect(500, 370, self.width, self.height)
        self.msg_image_rect.center = self.rect.center
        self.draw_button()

    def hard_button(self):
        """ This is the hard button. """
        self.rect = pygame.Rect(800, 370, self.width, self.height)
        self.msg_image_rect.center = self.rect.center
        self.draw_button()

    def draw_button(self):
        """ Draw blank button and then draw message. """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
