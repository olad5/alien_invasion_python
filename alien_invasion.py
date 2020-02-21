import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from rectangle import Rectangle


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
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.rectangle = Rectangle(self)

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

    def _check_keydown_events(self, event):
        """ Respond to keypresses. """
        # if event.key == pygame.K_RIGHT:
        #     self.ship.moving_right = True
        # elif event.key == pygame.K_LEFT:
        #     self.ship.moving_left = True
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
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """ Respond to bullet-alien collisions. """
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """ Update the postions of all aliens in the fleet. """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

            # Look for aliens hitting the bottom of the screen.
        self._check_aliens_left()

    def _update_box(self):
        """ Update the position of the box. """
        self._check_rect_edges()
        self.rectangle.update()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_rect_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        if self.rectangle.check_edges():
            print("jelly")
            self._change_box_direction()

    def _ship_hit(self):
        """ Respond to the ship being hit by an alien. """
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
            print(self.stats.ships_left)

        else:
            self.stats.game_active = False

    def _check_aliens_left(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.left <= screen_rect.left:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _change_box_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        self.rectangle.rect.y += self.settings.box_drop_speed
        self.settings.fleet_direction *= -1
        # print(self.rectangle.rect)

    def _create_fleet(self):
        """ Create the fleet of aliens. """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_y = self.settings.screen_height - alien_height
        number_aliens_y = available_space_y // (2 * alien_height)
        # print(number_aliens_y)

        # Determine the number of rows of aliens that fit on the screen.
        ship_width = self.ship.rect.width
        # available_space_x = self.settings.screen_width - (3 * alien_width) - ship_width
        available_space_x = self.settings.screen_width - (3 * alien_width) - ship_width
        youth = self.settings.screen_width - available_space_x
        number_rows = available_space_x // (2 * alien_width)
        # print(number_rows)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_y):
                self.__create_alien(alien_number, row_number)

    def __create_alien(self, alien_number, row_number):
        """ Create aan alien and place it in the row. """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.y = alien_height + 2 * alien_height * alien_number
        alien.rect.y = alien.y
        self.aliens.add(alien)
        # alien.rect.x = alien.rect.width + 2 * alien.rect.width * row_number
        alien.rect.x = self.settings.screen_width - 2 * alien.rect.width * row_number

    def _update_screen(self):
        """ Update images on the screen, amd flip to new screen """
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.rectangle.draw_rectangle()

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
