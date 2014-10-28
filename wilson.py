"""
A class that runs Wilson's algorithm to draw the maze.
Author: Brendan Wilson (no relation)
"""

import random
import walker_base
from maze_constants import *

class Wilson(walker_base.ArrayWalker):

    class Node(object):
        """Just a simple data container"""

        __slots__ = 'isOpen', 'direction'

        def __init__(self, isOpen, direction):
            self.isOpen = isOpen
            self.direction = direction

    def __init__(self, maze):
        super(Wilson, self).__init__(maze, maze.start())
        self.init_map(Node(False, None))

    def _plan(self, x, y):
        """Tries to find a route from a non-open cell back to an open one"""
        

    def build_maze(self):
        """Modifies the maze in place"""
        self._map[0][0].isOpen = True

        for x in xrange(XCELLS):
            for y in xrange(YCELLS):
                if not self._map[x][y].isOpen:
                    self._plan(x, y)
                    self._position = self._maze._get_cell(x, y)
                    self._dig()