"""
A class that runs Wilson's algorithm to draw the maze.
Author: Brendan Wilson (no relation)
"""

# This whole thing demands rabid rewriting, whenever I get around to it.
import random
from walker_base import WalkerBase
from maze_constants import *

class Wilson(WalkerBase):

    class Node(object):

        __slots__ = 'isOpen', 'next'

        def __init__(self, isOpen, next):
            self.isOpen = isOpen
            self.next = next

    def __init__(self, maze, loopProb=0):
        # loopProb should be between 0 and 1
        super(Wilson, self).__init__(maze, maze.start(), self.Node(False, None))
        self._open(self._maze.start())
        self._maze.paint(self._cell, OPEN_FILL)
        self.x = 0
        self.y = 0
        self._loopProb = loopProb
        #self._maze.update_idletasks()

    def _mark_next(self, cell, next):
        """Mark the direction gone on the map. Direction is a cell."""
        self.read_map(cell).next = next

    def _has_next(self, cell):
        """Check to see if the node here has a next other than None"""
        return self.read_map(cell).next is not None

    def _open(self, cell):
        self.read_map(cell).isOpen = True

    def _is_open(self, cell):
        return self.read_map(cell).isOpen

    def _erase_tracks(self, cell):
        """Follow the nexts and clean them up"""
        next = self.read_map(cell).next
        if next is None:
            return
        self._mark_next(cell, None)
        self._maze.paint(cell, NULL_FILL)
        self._erase_tracks(next)

    def _plan(self, cell):
        """Tries to find a route from a non-open cell back to an open one"""
        last = None
        while True:
            if not RUSH_WILSON:
                self._maze.paint(cell, PLAN_FILL)
                self._maze.update_idletasks()

            newCell = cell.random_path(last, checkWalls=False)
            self._mark_next(cell, newCell)

            if self.read_map(newCell).isOpen:   # success
                return
            elif self._has_next(newCell):
                # We need to clip off a portion of the path
                self._erase_tracks(newCell)

            last = cell
            cell = newCell

    def _dig(self):
        """There should be a good path from the current position back to
        the open part of the maze. This will then "dig" these cells open.
        """
        if self._is_open(self._cell):
            self._maze.paint(self._cell, OPEN_FILL)
            return

        self._open(self._cell)
        self._cell.open_by_cells(self.read_map(self._cell).next)
        self._maze.paint(self._cell, OPEN_FILL)

        self._cell = self.read_map(self._cell).next
        self._dig()

    def _open_deadend(self, cell):
        for path in DIRECTIONS:
            hall = cell.get_hall(path)
            if hall is not None and hall.is_open():
                deadend = cell.get_hall(OPPOSITES[path])
                if deadend is not None:
                    deadend.open_wall()

    def _add_braids(self):
        for row in self._maze.get_maze_array():
            for cell in row:
                if cell.count_halls() == 1 and \
                self._loopProb > random.random():
                    self._open_deadend(cell)
                    self.paint(cell, OPEN_FILL)
        self._maze.update_idletasks()

    def step(self):
        """Modifies the maze in place..
        """
        if self.x == XCELLS:
            self.x = 0
            self.y += 1
        if self.y == YCELLS:
            if self._loopProb > 0:
                self._add_braids()
            self._isDone = True
            return

        self._cell = self._maze.get_cell(self.x, self.y)
        if not self._is_open(self._cell):
            self._plan(self._cell)
            self._dig()
                
        self.x += 1 
