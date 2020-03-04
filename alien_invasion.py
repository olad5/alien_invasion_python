import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet

from alien import Alien
from game_stats import GameStats
from rectangle import Rectangle
from button import Button


class AlienInvasion:
    """ Overall class to manage game assets and behaviour """

    def __init__(self):
        """ Initialize the game, and create game resourcses. """
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")
        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        # self.aliens = pygame.sprite.Group()
        # self._create_fleet()

        # Make the moving box.
        self.rectangle = Rectangle(self)
        self.rect_list = pygame.sprite.Group()
        self.rect_list.add(self.rectangle)

        # Make the Play button.
        self.play_button = Button(self, "Play")

        # Make the multiple buttons
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium")
        self.hard_button = Button(self, "Hard")

        self.button_list = pygame.sprite.Group()

        self.button_list.add(self.easy_button)
        self.button_list.add(self.medium_button)
        self.button_list.add(self.hard_button)

    def run_game(self):
        """ Start the main loop for the game. """
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                # self._update_aliens()
                self._update_box()

            self._update_screen()

    def _check_events(self):
        """ Respond to keypresses and mouse events. """
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_pos = pygame.mouse.get_pos()
            #     self._check_play_button(mouse_pos)
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_pos = pygame.mouse.get_pos()
            #     self._check_easy_button(mouse_pos)
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     print("leg")
            #     mouse_pos = pygame.mouse.get_pos()
            #     self._check_medium_button(mouse_pos)
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_pos = pygame.mouse.get_pos()
            #     self._check_hard_button(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for value in range(1):
                    self._check_easy_button(mouse_pos)
                    self._check_medium_button(mouse_pos)
                    self._check_hard_button(mouse_pos)

    # def _check_play_button(self, mouse_pos):
    #     """ Start a new game when the player clicks Play. """
    #     button_clicked = self.play_button.rect.collidepoint(mouse_pos)
    #     # print(self.stats.game_active)
    #     if button_clicked and not self.stats.game_active:
    #         # Reset the game settings.
    #         self.settings.initialize_dynamic_settings()
    #         # Reset the game statistics.
    #         self.stats.reset_stats()
    #         self.stats.game_active = True

    #         # Get rid of any remaining aliens and bullets.
    #         # self.aliens.empty()
    #         self.bullets.empty()

    #         # Create a new fleet and center the ship
    #         # self._create_fleet()
    #         self.ship.center_ship()

    #         # Hide the mouse cursor.
    #         pygame.mouse.set_visible(False)

    def _general_settings(self):
        """ General settings for all the difficulty levels. """
        # Reset the game settings.
        # self.settings.initialize_dynamic_settings()
        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True

        # Get rid of any remaining aliens and bullets.
        # self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship
        # self._create_fleet()
        self.ship.center_ship()

        self.settings.fleet_direction = 1
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _check_easy_button(self, mouse_pos):
        """ Start new game in easy mode. """
        easy_mode = self.easy_button.rect.collidepoint(mouse_pos)
        if easy_mode and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self._general_settings()

    def _check_medium_button(self, mouse_pos):
        """ Start new game in medium mode. """
        medium_mode = self.medium_button.rect.collidepoint(mouse_pos)
        if medium_mode and not self.stats.game_active:
            self.settings.ship_speed = 1.5
            self.settings.bullet_speed = 1.5
            # Box settings
            self.settings.box_drop_speed = 1.2

            self._general_settings()

    def _check_hard_button(self, mouse_pos):
        """ Start new game in hard mode. """
        hard_mode = self.hard_button.rect.collidepoint(mouse_pos)
        if hard_mode and not self.stats.game_active:
            self.settings.ship_speed = 1.5
            self.settings.bullet_speed = 1.7
            # Box settings
            self.settings.box_drop_speed = 1.5

            self._general_settings()

    def _check_keydown_events(self, event):
        """ Respond to keypresses. """
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """ Respond to key releases. """
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullets group. """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ Update position of bullets and get rid of old bullets. """
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.right >= self.settings.screen_width:
                # self._check_bullet_box_collisions()
                self.bullets.remove(bullet)
            self._check_bullet_box_collisions()

    def _check_bullet_box_collisions(self):
        """ Respond to bullet-box collisions. """
        # Remove any bullets and aliens that have collided.
        # collisions = pygame.sprite.spritecollideany(self.rectangle, self.bullets)
        # print(self.bullets)
        hit = pygame.sprite.groupcollide(self.bullets, self.rect_list, True, False)
        # print(hit)
        for rec in self.rect_list:
            # print(rec.rect.right)
            for bullet in self.bullets.copy():
                # print(not hit)
                end = bullet.rect.right >= (self.settings.screen_width - 1)
                # print(end)
                if hit and (bullet.rect.right <= rec.rect.right) and (not end):
                    print("Try to miss")
                    # sleep(0.5)
                    self.settings.increase_speed()
                    print(self.settings.box_drop_speed)
                    break

                elif (not hit) and (
                    bullet.rect.right >= (self.settings.screen_width - 1)
                ):
                    # print("leggo")
                    self.settings.ship_limit -= 1
                    # print(self.settings.ship_limit)
                    self.bullets.empty()
                    if self.settings.ship_limit < 0:
                        self.stats.game_active = False
                        pygame.mouse.set_visible(True)
                        self.stats.reset_stats()

    def _update_box(self):
        """ Update the position of the box. """
        self._check_rect_edges()
        self.rectangle.update()

    def _check_rect_edges(self):
        """Respond appropriately if the box has reached an edge."""
        if self.rectangle.check_edges():
            self._change_box_direction()

    def _ship_hit(self):
        """ Respond to the ship being hit by an alien. """
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and bullets
            # self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            # self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
            print(self.stats.ships_left)

        else:
            print("out of lives")
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _change_box_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        # self.rectangle.rect.x -= self.settings.box_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """ Update images on the screen, amd flip to new screen """
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # self.aliens.draw(self.screen)
        # for rec in self.rect_list.sprites():
        #     print(rec)
        self.rectangle.draw_rectangle()
        # self.rectangle.Group.draw()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            # print(self.button_list)
            # self.play_button.draw_button()
            # for value in range(len(self.button_list)):
            self.easy_button.easy_button()
            self.medium_button.medium_button()
            self.hard_button.hard_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
