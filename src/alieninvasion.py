import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


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

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()


	def _create_fleet(self):

		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2*alien_width)
		n_aliens_x = available_space_x // (2*alien_width)

		ship_height = self.ship.rect.height
		available_space_y = self.settings.screen_height - 3*alien_height - ship_height
		n_rows = available_space_y // (2*alien_height)

		for row in range(n_rows):
			for col in range(n_aliens_x):
				self._create_alien(col, row)


	def _create_alien(self, col, row):

		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2*alien_width*col
		alien.rect.x = alien.x
		alien.rect.y = alien_height + 2*alien_height*row
		self.aliens.add(alien)


	def run_game(self):

		while True:
			self._check_events()
			self.ship.update()
			self._update_bullets()
			self._update_screen()


	def _check_events(self):

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)


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


	def _update_screen(self):

		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		#Draw each alien in the group
		self.aliens.draw(self.screen)

		pygame.display.flip()


if __name__ == "__main__":

	ai = AlienInvasion()
	ai.run_game()