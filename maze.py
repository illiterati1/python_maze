"""
The class file for the maze, as well as the cells within the maze.
Author: Brendan Wilson
"""

from maze_constants import *

class Cell(object):
    """north, east, south, and west will be references to other Cells.
    This class will probably just be passed in to the drawing
    function to deal with displaying the maze."""

    __slots__ = '_directions', '_visited', '_xLoc', '_yLoc'

    case = {'north': 0, 'east': 1, 'south': 2, 'west': 3}
    opposite = {'north': 'south', 'east': 'west', 'south': 'north', \
                'west': 'east'}

    def __init__(self, x, y, north=False, east=False, south=False, west=False):
        self._xLoc = x
        self._yLoc = y
        self._directions = [north, east, south, west]
        self._visited = False

    def visit(self):
        self._visited = True

    def unvisit(self):
        self._visited = False

    def visited(self):
        return self._visited

    def set_direction(self, direction):
        """direction must be 'north', 'east', etc."""
        self._directions[Cell.case[direction]] = True

    def get_direction(self, direction):
        """See above"""
        return self._directions[Cell.case[direction]]

    def get_position(self):
        """Return the x, y position of the top left corner as a tuple"""
        return self._xLoc, self._yLoc

    def get_links(self):
        """Returns the entire direction list"""
        return self._directions

    def is_junction(self):
        return self._directions.count(True) > 2

class Maze(object):

    def __init__(self):
        self._cells = [[Cell(x, y) for y in xrange(0, MAZE_HEIGHT, CELL_SIZE)]\
                        for x in xrange(0, MAZE_WIDTH, CELL_SIZE)]

    def get_cell(self, x, y):
        """Returns the cell at position x, y.
        x and y are in terms of cell numbers, not pixels"""
        return

if __name__ == '__main__':
    maze = Maze()