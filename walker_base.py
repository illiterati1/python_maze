"""
A collection of abstract-ish classes for the maze walker classes
Author: Brendan Wilson
"""

import copy
from maze_constants import *

class WalkerBase(object):
    """The grandparent of all walkers"""

    movement = {'north': (lambda x, y: (x, y-1)), \
                'east': (lambda x, y: (x+1, y)), \
                'south': (lambda x, y: (x, y+1)), \
                'west': (lambda x, y: (x-1, y))}

    def __init__(self, maze, position):
        """Takes a cell object from the maze in question"""
        self._maze = maze
        self._position = position   # This is a cell object

    def move(self, direction):
        """Move in the indicated direction"""
        self._position = self._maze._move(self._position, direction)

    def paint(self, cell, color, redraw=True, changeWalls=True):
        """Paint the current cell the indicated color"""
        self._maze.paint(self._position, color)

    def location(self):
        """Return (x, y) of current location in the maze"""
        return self._position.get_position()

class ArrayWalker(WalkerBase):
    """A maze walker that stores it's knowledge of the maze in an array
    that has a one-to-one correspondence to the maze."""

    def __init__(self, maze, position, default):
        super(ArrayWalker, self).__init__(maze, position)
        self._map = [[copy.copy(default) for y in xrange(YCELLS)] \
                     for x in xrange(XCELLS)]

    def init_map(self, default):
        """Set each point on the map to some default value"""
        for row in xrange(len(self._map)):
            for col in xrange(len(self._map[row])):
                self._map[row][col] = copy.copy(default)

    def mark_current(self, mark):
        """Mark the location with whatever data the child class needs.
        mark() should be a function that operates on the cell."""
        self.mark_this(self._position, mark)

    def mark_this(self, cell, mark):
        """Mark the cell indicated. Cell must be a cell object."""
        x, y = cell.get_position()
        mark(self._map[x][y])

    def read_map(self, x, y):
        """Return the info about the current cell"""
        return self._map[x][y]

class LinkWalker(WalkerBase):
    """A walker class that keeps information about links between junctions.
    Only used for the Tremaux algorithm."""

    class Node(object):
        """An object for storing the knowledge of the LinkWalkers.
        Little more than a structure."""

        __slots__ = 'cell', 'north', 'east', 'south', 'west'

        def __init__(self, cell, north=None, east=None, south=None, west=None):
            self.cell = cell
            self.north = north
            self.east = east
            self.south = south
            self.west = west

    def __init__(self, maze, position):
        super(LinkWalker, self).__init__(maze, position)
