"""
A breadth first search walker.
Author: Brendan Wilson
"""

from Queue import Queue
from maze_constants import *
import walker_base

SEARCH_COLOR = 'gray70'
marker = object()

class BreadthWalker(walker_base.ArrayWalker):

    class Node(object):
        __slots__ = 'previous'

        def __init__(self):
            self.previous = None

    def __init__(self, maze):
        super(BreadthWalker, self).__init__(maze, maze.start(), self.Node())
        self._maze.clean()
        self.queue = Queue()
        self.queue.put(self._position)
        self.queue.put(marker)

    def _get_next(self):
        """This is necessary because .get() will wait forever if the queue 
        is empty
        """
        if self.queue.empty():
            return None
        else:
            return self.queue.get()

    def _make_mark(self, direction):
        """A helper function to make marks on the map"""
        def mark(node):
            node.previous = direction
        return mark

    def walk(self):
        position = self._get_next()
        hitMarker = False
        while position is not self._maze.finish():
            if position is marker:
                hitMarker = True
                self.queue.put(marker)
                position = self._get_next()
                continue
            elif position is None:
                raise ValueError('No solution to maze')

            self.paint(position, SEARCH_COLOR, redraw=hitMarker)
            hitMarker = False

            for direction in position.open_paths():
                newPosition = self._maze._move(position, direction)
                if self.read_map(newPosition).previous is None:
                    self.mark_this(newPosition, self._make_mark(OPPOSITES[direction]))
                    self.queue.put(newPosition)
            position = self._get_next()