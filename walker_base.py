"""
A parent class for all the walkers.

Copyright (C) 2014 Brendan Wilson
brendan.x.wilson@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import copy
from maze_constants import *

class WalkerBase(object):
    """The parent of all walkers"""

    def __init__(self, maze, position, default=object):
        """Takes a cell object from the maze in question
        NOTE: default must not be object if you want a map of any kind.
        """
        self._delay = DELAY
        self._isDone = False
        self._maze = maze
        self._cell = position   # This is a cell object
        if default is not object:
            # TODO: get rid of copy by changing default to function call
            self._map = [[copy.deepcopy(default) for y in xrange(YCELLS)] \
                         for x in xrange(XCELLS)]

    def delay(self):
        return self._delay

    def is_done(self):
        return self._isDone

    def step(self):
        """An abstract method to use with Tkinter so that the walker returns
        control back to the main loop every so often. Should return False
        when the walker is finished."""
        raise NotImplementedError()

    def paint(self, cell, color, paintWalls=True):
        """Paint the current cell the indicated color"""
        self._maze.paint(cell, color, paintWalls)

    def init_map(self, default):
        """Set each point on the map to some default value"""
        for row in xrange(len(self._map)):
            for col in xrange(len(self._map[row])):
                self._map[row][col] = copy.copy(default)

    # The next three are depracated
    def mark_current(self, mark):
        """Mark the location with whatever data the child class needs.
        mark() should be a function that operates on the cell."""
        self.mark_this(self._cell, mark)

    def mark_this(self, cell, mark):
        """Mark the cell indicated. Cell must be a cell object."""
        x, y = cell.get_position()
        mark(self._map[x][y])

    def read_current(self):
        """Get the map data for the current cell."""
        return self.read_map(self._cell)

    def read_map(self, cell):
        """Return the info about the current cell"""
        x, y = cell.get_position()
        return self._map[x][y]
