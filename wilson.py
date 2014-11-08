"""
A class that runs Wilson's algorithm to draw the maze.
Author: Brendan Wilson (no relation)
"""

import random
import walker_base
from maze_constants import *

class Wilson(walker_base.ArrayWalker):

    class Node(object):
        """Just a simple data container"""

        __slots__ = 'isOpen', 'direction'

        def __init__(self, isOpen, direction):
            self.isOpen = isOpen
            self.direction = direction

    directions = walker_base.WalkerBase.movement.keys()

    def __init__(self, maze):
        super(Wilson, self).__init__(maze, maze.start(), self.Node(False, None))

    def _is_valid(self, x, y):
        """Make sure a cell is in bounds"""
        return 0 <= x < XCELLS and 0 <= y < YCELLS

    def _mark_direction(self, x, y, direction):
        """Mark the direction gone on the map"""
        self._map[x][y].direction = direction

    def _has_direction(self, x, y):
        """Check to see if the node here has a direction other than None"""
        return self._map[x][y].direction != None

    def _get_direction(self, x, y):
        return self._map[x][y].direction

    def _is_open(self, x, y):
        """Check to see if the given node has been dug out already"""
        return self._map[x][y].isOpen

    def _open(self, x, y):
        self._map[x][y].isOpen = True

    def _erase_tracks(self, x, y):
        """Follow the directions left and clean them up"""
        direction = self._get_direction(x, y)
        if direction == None:
            return
        self._mark_direction(x, y, None)
        self._maze.paint(self._maze._get_cell(x, y), NULL_FILL, False)
        newX, newY = walker_base.WalkerBase.movement[direction](x, y)
        self._erase_tracks(newX, newY)

    def _plan(self, x, y):
        """Tries to find a route from a non-open cell back to an open one"""
        counter = 0
        while True:
            if not RUSH_WILSON:
                self._maze.paint(self._maze._get_cell(x, y), PLAN_FILL, counter % 50 == 0)
            counter += 1
            randInt = random.randrange(0, 4)    # will be 0, 1, 2, or 3
            newX, newY = walker_base.WalkerBase.movement[Wilson.directions[randInt]](x, y)
            while (newX, newY) == (x, y) or not self._is_valid(newX, newY):
                randInt = (randInt + 1) % len(Wilson.directions)
                newX, newY = walker_base.WalkerBase.movement[Wilson.directions[randInt]](x, y)

            self._mark_direction(x, y, Wilson.directions[randInt])

            if self._is_open(newX, newY):   # success
                return
            elif self._has_direction(newX, newY):
                # We need to clip off a portion of the direction list
                self._erase_tracks(newX, newY)

            x, y = newX, newY

    def _dig(self):
        """There should be a good path from the current position back to
        the open part of the maze. This will then "dig" these cells open.
        """

        x, y = self._position.get_position()
        direction = self._get_direction(x, y)
        if self._is_open(x, y):
            self._maze.paint(self._position, OPEN_FILL)
            return

        self._open(x, y)
        self._maze._join_cells(self._position, direction)
        self._maze.paint(self._position, OPEN_FILL, False)

        self.move(direction)
        self._dig()

    def build_maze(self):
        """Modifies the maze in place"""
        self._open(0, 0)
        self._maze.paint(self._position, OPEN_FILL)

        for y in xrange(YCELLS):
            for x in xrange(XCELLS):
                if not self._map[x][y].isOpen:
                    self._plan(x, y)
                    self._position = self._maze._get_cell(x, y)
                    self._dig()