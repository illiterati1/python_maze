"""
A collection of abstract-ish classes for the maze walker classes
Author: Brendan Wilson
"""

class WalkerBase(object):
	"""The grandparent of all walkers"""

	def __init__(self, maze, position):
		"""Takes a cell object from the maze in question"""
		self._maze = maze
		self._position = position

	def move(self, direction):
		"""Move in the indicated direction"""
		self._position = 
