"""
A class that runs Wilson's algorithm to draw the maze.
Author: Brendan Wilson (no relation)
"""

import walker_base

class Wilson(walker_base.ArrayWalker):

    class Node(object):
        """Just a simple data container"""

        __slots__ = 'isOpen', 'direction'

        def __init__(self, isOpen, direction):
            self.isOpen = isOpen
            self.direction = direction

    def __init__(self, maze):
        super(Wilson, self).__init__(maze, maze.start())
        self.init_map()     # We will only store directions as needed

    def _tunnel(self):
        pass

    def build_maze(self):
        """Modifies the maze in place"""
        