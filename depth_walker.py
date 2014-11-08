"""
Depth first recursion solver
Author: Brendan Wilson
"""

import random
import walker_base
from maze_constants import *

SEARCH_COLOR = 'blue'
FOUND_COLOR = 'red'
VISITED_COLOR = 'grey'

class DepthWalker(walker_base.ArrayWalker):

    class Node(object):

        __slots__ = 'visited'

        def __init__(self, visited):
            self.visited = visited

    def __init__(self, maze):
        super(DepthWalker, self).__init__(maze, maze.start(), self.Node(False))
        self._maze.clean()
        self.mark_current(self._visit)

    def _visit(self, node):
        node.visited = True

    def _unvisit(self, node):
        node.visited = False

    def walk(self):
        if self._position is self._maze.finish():
            self.paint(self._position, FOUND_COLOR, changeWalls=False)
            return True
        self.mark_current(self._visit)
        self.paint(self._position, SEARCH_COLOR)

        paths = self._position.open_paths()

        for direction in paths:
            x, y = self._position.get_position()
            x, y = walker_base.WalkerBase.movement[direction](x, y)
            if not self.read_map(x, y).visited:
                self.move(direction)
                found = self.walk()
                self.move(OPPOSITES[direction])
                if found:
                    self.paint(self._position, FOUND_COLOR, changeWalls=False)
                    return found
        self.paint(self._position, VISITED_COLOR)
        return False