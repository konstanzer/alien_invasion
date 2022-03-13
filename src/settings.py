class Settings:
	"""Settings for Alien Invasion"""

	def __init__(self):

		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)
		#Ship
		self.ship_speed = 1.5
		#Bullets
		self.bullet_speed = 1.
		self.bullet_width = 3
		self.bullet_height = 12
		self.bullet_color = (60, 60, 60)
		self.bullet_limit = 3