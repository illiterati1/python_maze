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

    def __init__(self, maze):
        super(Wilson, self).__init__(maze, maze.start(), self.Node(False, None))
        self._open(self._maze.start())
        self._maze.paint(self._cell, OPEN_FILL)
        self.x = 0
        self.y = 0
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

    def step(self):
        """Modifies the maze in place..
        """
        if self.x == XCELLS:
            self.x = 0
            self.y += 1
        if self.y == YCELLS:
            self._isDone = True
            return
        self._cell = self._maze.get_cell(self.x, self.y)
        if not self._is_open(self._cell):
            self._plan(self._cell)
            self._dig()
        self.x += 1
        
        """
        
        for y in xrange(YCELLS):
            for x in xrange(XCELLS):
                if self._cell is not self._maze.get_cell(x, y):
                    self._cell = self._maze.get_cell(x, y)
                if not self._is_open(self._cell):
                    self._plan(self._cell)
                    self._dig()
                    self._maze.update_idletasks()"""    

class LoopyWilson(Wilson):
    """A maze builder that will add loops to the maze"""

    def _find_walls(self, cell):
        directions = []
        x, y = cell.get_position()
        for direction, isOpen in cell.get_links().items():
            if not isOpen:     # If there is a wall
                newX, newY = walker_base.WalkerBase.movement[direction](x, y)
                if self._is_valid(newX, newY):
                    directions.append(direction)
        return directions

    def _find_deadend(self, cell):
        """Assumes that cell is a deadend"""
        possibles = ['north', 'east', 'south', 'west']
        links = cell.get_links()
        x, y = cell.get_position()
        for i in xrange(len(possibles)):
            left = possibles[i-1]
            center = possibles[i]
            right = possibles[(i+1) % len(possibles)]
            if not (links[left] or links[right] or links[center]):
                newX, newY = walker_base.WalkerBase.movement[center](x, y)
                if self._is_valid(newX, newY):
                    return center
        return None

    def build_maze(self):
        super(LoopyWilson, self).build_maze()
        for col in self._maze._get_maze_array():
            for cell in col:
                if cell.count_halls() == 1 and random.random() <= LOOP_PROB:
                    direction = self._find_deadend(cell)
                    if direction is not None:
                        self._maze._join_cells(cell, direction)
                        self.paint(cell, OPEN_FILL)

