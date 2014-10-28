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

    movement = {'north': (lambda x, y: (x, y-1)),
                'east': (lambda x, y: (x+1, y)),
                'south': (lambda x, y: (x, y+1)),
                'west': (lambda x, y: (x-1, y))}

    directions = movement.keys()

    def __init__(self, maze):
        super(Wilson, self).__init__(maze, maze.start())
        self.init_map(Node(False, None))

    def _is_valid(self, x, y):
        """Make sure a cell is in bounds"""
        return x < 0 or x >= XCELLS or y < 0 or y >= YCELLS

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

    def _erase_tracks(self, x, y):
        """Follow the directions left and clean them up"""
        direction = self._get_direction(x, y)
        if direction == None:
            return
        self._mark_direction(x, y, None)
        self._maze._get_cell(x, y).paint(NULL_FILL)
        newX, newY = Wilson.movement[direction](x, y)
        self._erase_tracks(newX, newY)

    def _plan(self, x, y):
        """Tries to find a route from a non-open cell back to an open one"""

        self._maze._get_cell(x, y).paint(PLAN_FILL)
        randInt = random.randrange(0, 4)    # will be 0, 1, 2, or 3
        newX, newY = Wilson.movement[Wilson.directions[randInt]](x, y)
        while not self._is_valid(newX, newY):   # check clockwise for good dir
            randInt = (randInt + 1) % len(directions)
            newX, newY = Wilson.movement[Wilson.directions[randInt]](x, y)

        self._mark_direction(x, y, Wilson.directions[randInt])

        if self._is_open(newX, newY):   # success
            return
        elif self._has_direction(newX, newY):
            # We need to clip off a portion of the direction list
            self._erase_tracks(newX, newY)

        self._plan(newX, newY)

    def build_maze(self):
        """Modifies the maze in place"""
        self._map[0][0].isOpen = True

        for x in xrange(XCELLS):
            for y in xrange(YCELLS):
                if not self._map[x][y].isOpen:
                    self._plan(x, y)
                    self._position = self._maze._get_cell(x, y)
                    self._dig()