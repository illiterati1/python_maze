"""
A breadth first search walker.
Author: Brendan Wilson
"""

from Queue import Queue
from maze_constants import *
import walker_base

class SearchColors(object):
    colors = ['gray80', 'gray78', 'gray76', 'gray74', 'gray72', 'gray70', \
              'gray68', 'gray66', 'gray64', 'gray62', 'gray60']

    def __init__(self):
        assert len(SearchColors.colors) > 1
        self.index = 0
        self.step = 1

    def color(self):
        return SearchColors.colors[self.index]

    def next(self):
        if self.index == len(SearchColors.colors) - 1:
            self.step = -1
        elif self.index == 0:
            self.step = 1
        self.index += self.step


SEARCH_COLORS = SearchColors()
FOUND_COLOR = 'red'
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
                SEARCH_COLORS.next()
                continue

            self.paint(position, SEARCH_COLORS.color(), redraw=hitMarker)
            hitMarker = False

            for direction in position.open_paths():
                newPosition = self._maze._move(position, direction)
                if self.read_map(newPosition).previous is None:
                    self.mark_this(newPosition, self._make_mark(OPPOSITES[direction]))
                    self.queue.put(newPosition)
            position = self._get_next()

        while position is not self._maze.start():
            self.paint(position, FOUND_COLOR)
            direction = self.read_map(position).previous
            position = self._maze._move(position, direction)
        self.paint(position, FOUND_COLOR)
