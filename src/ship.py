import pygame
from os.path import dirname, abspath, join

#Parent directory
path = dirname(dirname(abspath(__file__)))

class Ship:
	"""The player's ship"""

	def __init__(self, ai_game):

		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

		self.image = pygame.image.load(join(path, "img", "ship.bmp"))
		self.rect = self.image.get_rect()
		self.rect.midbottom = self.screen_rect.midbottom

		#Decimal value for ship's horizontal position
		self.x = float(self.rect.x)
		
		# Movement flags
		self.moving_right = False
		self.moving_left = False


	def update(self):

		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed

		self.rect.x = self.x


	def blitme(self):
		"""Draw ship at new loaction"""
		self.screen.blit(self.image, self.rect)