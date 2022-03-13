import pygame
from pygame.sprite import Sprite
from os.path import dirname, abspath, join
path = dirname(dirname(abspath(__file__)))

class Alien(Sprite):
	"""A single alien"""

	def __init__(self, ai_game):
		
		super().__init__()
		self.screen = ai_game.screen

		self.image = pygame.image.load(join(path, "img", "alien.bmp"))
		self.rect = self.image.get_rect()

		#Start position
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#Decimal value for horizontal position
		self.x = float(self.rect.x)