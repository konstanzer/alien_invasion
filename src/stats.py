class Stats:
	"""Track statistics"""
	def __init__(self, ai_game):

		self.settings = ai_game.settings
		self.reset_stats()
		self.game_active = False

		with open('high_score.txt') as f:
			self.high_score = int(f.readline())

	def reset_stats(self):
		"""Reset variable stats"""
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1