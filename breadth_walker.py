"""
A breadth first search walker.
Author: Brendan Wilson
"""

from Queue import Queue
from maze_constants import *
import walker_base

SEARCH_COLOR = 'grey'

class BreadthWalker(walker_base.ArrayWalker):

    def Node(object):
        __slots__ = 'previous'

        def __init__(self):
            self.previous = None

    def __init__(self, maze):
        super(BreadthWalker, self).__init__(maze, maze.start(), Node())
        self._maze.clean()
        self.queue = Queue()
        self.queue.put(self._position)

    def _get_next(self):
        if self.queue.empty():
            return None
        else:
            return self.queue.get()

    def walk(self):
        position = self._get_next()
        if position is None:
            raise ValueError('No solution to maze')

        self.paint(position, SEARCH_COLOR)

        for direction in position.open_paths():
            position = self._maze._move(position, direction)
            if self.read_map(position).previous is None:
                self.mark_this(position, lambda x: x = direction)