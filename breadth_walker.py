"""
A breadth first search walker.
Author: Brendan Wilson
"""

from Queue import Queue
from maze_constants import *
import walker_base
from maze_pieces import MazeError

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

class BreadthWalker(walker_base.WalkerBase):

    class Node(object):
        __slots__ = 'previous'

        def __init__(self):
            self.previous = None

    def __init__(self, maze):
        super(BreadthWalker, self).__init__(maze, maze.start(), self.Node())
        self._maze.clean()
        self.queue = Queue()
        self.queue.put(self._cell)
        self.queue.put(marker)

    def _get_next(self):
        """This is necessary because .get() will wait forever if the queue 
        is empty
        """
        if self.queue.empty():
            return None
        else:
            return self.queue.get()

    def _make_mark(self, fromCell, toCell):
        """A helper function to make marks on the map"""
        self.read_map(toCell).previous = fromCell

    def step(self):
        cell = self._get_next()
        hitMarker = False
        while cell is not self._maze.finish():
            if cell is marker:
                hitMarker = True
                self.queue.put(marker)
                cell = self._get_next()
                SEARCH_COLORS.next()
                continue

            self._maze.paint(cell, SEARCH_COLORS.color())
            if hitMarker:
                self._maze.update_idletasks()
                hitMarker = False

            for newCell in cell.get_paths(last=self.read_map(cell).previous):
                if self.read_map(newCell).previous is None:
                    # Only worry about unvisited cells
                    self._make_mark(cell, newCell)
                    self.queue.put(newCell)
            cell = self._get_next()

        while cell is not None:
            # Start cell should point to None
            self._maze.paint(cell, FOUND_COLOR)
            cell = self.read_map(cell).previous
        self._maze.update_idletasks()
