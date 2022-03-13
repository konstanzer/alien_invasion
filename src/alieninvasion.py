import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from stats import Stats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
	"""Parent class to manage game behavior"""
	
	def __init__(self):

		pygame.init()

		self.settings = Settings()

		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height

		self.bg_color = (230, 230, 230)
		pygame.display.set_caption("Alien Invasion")
		
		self.stats = Stats(self)
		self.sb = Scoreboard(self)
		self.ship = Ship(self)

		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		self.play_button = Button(self, "Play")


	def _create_fleet(self):

		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2*alien_width)
		n_aliens_x = available_space_x // (2*alien_width)

		ship_height = self.ship.rect.height
		available_space_y = self.settings.screen_height - 3*alien_height - ship_height
		#Scale divisor to limit rows.
		n_rows = available_space_y // (3*alien_height)

		for row in range(n_rows):
			for col in range(n_aliens_x):
				self._create_alien(col, row)


	def _create_alien(self, col, row):

		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2*alien_width*col
		alien.rect.x = alien.x
		#Scale height up to lower ships.
		alien.rect.y = alien_height*5 + 2*alien_height*row
		self.aliens.add(alien)


	def _check_fleet_edges(self):

		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break


	def _change_fleet_direction(self):

		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1


	def run_game(self):

		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

			self._update_screen()


	def _check_events(self):

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)


	def _check_play_button(self, mouse_pos):

		clicked = self.play_button.rect.collidepoint(mouse_pos)

		if clicked and not self.stats.game_active:
			self.settings.initialize_dynamic_settings()
			pygame.mouse.set_visible(False)
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()
			self.aliens.empty()
			self.bullets.empty()
			self._create_fleet()
			self.ship.center_ship()


	def _check_keydown_events(self, event):

		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()


	def _check_keyup_events(self, event):

		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False


	def _fire_bullet(self):

		if len(self.bullets) < self.settings.bullet_limit:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet) #add bullet to to bullets group


	def _update_bullets(self):

		self.bullets.update()

		#Delete bullets off screen
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()


	def _check_bullet_alien_collisions(self):
		#Whenever the rects of a bullet and alien overlap, groupcollide() adds a key-value pair to the dictionary it returns. The two True arguments tell Pygame to delete the bullets and aliens that have collided.
		#Set first boolean to False for piercing bullets
		collisions = pygame.sprite.groupcollide(self.bullets,
			self.aliens, True, True)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.aliens:
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()
			self.stats.level += 1
			self.sb.prep_level()


	def _update_aliens(self):

		self._check_fleet_edges()
		self.aliens.update()

		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		self._check_aliens_bottom()


	def _ship_hit(self):

		if self.stats.ships_left > 0:
			self.stats.ships_left -= 1
			self.sb.prep_ships()
			self.aliens.empty()
			self.bullets.empty()
			self._create_fleet()
			self.ship.center_ship()
			sleep(.5)
		else:
			self.stats.game_active = False

			if self.stats.score >= self.stats.high_score:
				with open('high_score.txt', 'w') as f:
					f.write(str(self.stats.score))

			pygame.mouse.set_visible(True)


	def _check_aliens_bottom(self):

		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				self._ship_hit()
				break


	def _update_screen(self):

		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()

		#Draw each alien in the group
		self.aliens.draw(self.screen)
		self.sb.show_score()

		if not self.stats.game_active:
			self.play_button.draw_button()

		pygame.display.flip()


if __name__ == "__main__":

	ai = AlienInvasion()
	ai.run_game()