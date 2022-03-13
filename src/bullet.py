import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
	"""Projectiles fired from ship. The Bullet class inherits from Sprite, which we import from the pygame .sprite module. When you use sprites, you can group related elements in your game and act on all the grouped elements at once. To create a bullet instance, __init__() needs the current instance of AlienInvasion, and we call super() to inherit properly from Sprite."""

	def __init__(self, ai_game):

		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color

		self.rect = pygame.Rect(0, 0,
			self.settings.bullet_width, self.settings.bullet_height)
		self.rect.midtop = ai_game.ship.rect.midtop

		self.y = float(self.rect.y)