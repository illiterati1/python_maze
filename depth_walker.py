"""
Depth first recursion solver
Author: Brendan Wilson
"""

import random
import walker_base
from maze_constants import *

SEARCH_COLOR = 'light blue'
FOUND_COLOR = 'red'
VISITED_COLOR = 'gray70'

class DepthWalker(walker_base.WalkerBase):

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

    def step(self, cell=None, last=None):
        if cell is None:
            cell = self._maze.start()
        if cell is self._maze.finish():
            self.paint(cell, FOUND_COLOR)
            return True

        self.mark_current(self._visit)
        self.paint(cell, SEARCH_COLOR)
        self._maze.update_idletasks()

        paths = cell.get_paths(last)

        for newCell in paths:
            if not self.read_map(newCell).visited:
                found = self.step(newCell, cell)
                if found:
                    self.paint(cell, FOUND_COLOR)
                    if cell is self._maze.start():
                        self._maze.update_idletasks()
                    return found
        self.paint(cell, VISITED_COLOR)
        return False