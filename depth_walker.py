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

        __slots__ = 'parent', 'visited'

        def __init__(self):
            self.parent = None
            self.visited = False

    def __init__(self, maze):
        super(DepthWalker, self).__init__(maze, maze.start(), self.Node())
        self._maze.clean()
        self._stack = [self._cell]

    def step(self):
        current = self._stack[-1]
        self.paint(current, SEARCH_COLOR)
        self.read_map(current).visited = True

        if current is self._maze.finish():
            self._isDone = True
            while current is not None:
                self.paint(current, FOUND_COLOR)
                current = self.read_map(current).parent
            return

        paths = current.get_paths(last=self.read_map(current).parent)
        paths = filter((lambda c: self.read_map(c).visited is False), paths)
        random.shuffle(paths)   # Make the path selection random

        if len(paths) == 0:
            # We've found a deadend essentially
            self.paint(current, VISITED_COLOR)
            self._stack.pop()
            return

        for cell in paths:
            self.read_map(cell).parent = current
            self._stack.append(cell)
