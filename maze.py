"""
The class file for the maze, as well as the cells within the maze.
Author: Brendan Wilson
"""

from maze_constants import *

class WallError(Exception):
    def __init__(self, error):
        self.message = error

class Maze(object):

    class Cell(object):
        """north, east, south, and west will be references to other Cells.
        This class will probably just be passed in to the drawing
        function to deal with displaying the maze."""

        __slots__ = '_directions', '_xLoc', '_yLoc'


        case = {'north': 0, 'east': 1, 'south': 2, 'west': 3}

        def __init__(self, x, y, \
                     north=False, east=False, south=False, west=False):
            self._xLoc = x
            self._yLoc = y
            self._directions = [north, east, south, west]

        def open_wall(self, direction):
            """direction must be 'north', 'east', etc."""
            self._directions[Cell.case[direction]] = True

        def is_open(self, direction):
            """Checks whether the given direction is open"""
            return self._directions[Cell.case[direction]]

        def get_position(self):
            """Return the x, y position of the cell as a tuple"""
            return self._xLoc, self._yLoc

        def get_links(self):
            """Returns the entire direction list"""
            return self._directions

        def is_junction(self):
            return self._directions.count(True) > 2

        def is_deadend(self):
            return self._directions.count(True) == 1

        def is_isolated(self):
            """For determining if the cell has no connections"""
            return self._directions.count(True) == 0

        def is_hallway(self):
            return self._directions.count(True) == 2

    movement = {'north': (lambda x, y: (x, y-1)),
                'east': (lambda x, y: (x+1, y)),
                'south': (lambda x, y: (x, y+1)),
                'west': (lambda x, y: (x-1, y))}

    opposite = {'north': 'south', 'east': 'west', 'south': 'north', \
                'west': 'east'}

    def __init__(self):
        self._cells = [[Cell(x, y) \
                        for y in xrange(MAZE_HEIGHT/CELL_SIZE)] \
                        for x in xrange(MAZE_WIDTH/CELL_SIZE)]

    def _get_cell(self, x, y):
        """Returns the cell at position x, y.
        x and y are in terms of cell numbers, not pixels"""
        return self._cells[x][y]

    def _clip(self, cell, direction):
        """Returns the cell in the given direction, regardless of walls.
        Raises WallError if cell is out of bounds."""
        currentX, currentY = cell.get_position()
        newX, newY = Maze.movement[direction](currentX, currentY)
        if newX < 0 or newX >= MAZE_WIDTH/CELL_SIZE \
           or newY < 0 or newY >= MAZE_HEIGHT/CELL_SIZE:
           raise WallError('Out of bounds')
        return self._get_cell(newX, newY) 


    def _join_cells(self, cell, direction):
        """Opens the wall between the cell given and the one in the
        given direction.
        """
        cell.open_wall(direction)
        self._clip(cell, direction).open_wall(opposite[direction])
        # The above line will return a WallError if an out of bounds cell
        # is used

    def _move(self, cell, direction):
        """Movement with wall checking"""
        if cell.is_open(direction):
            return self._clip(cell, direction)
        else:
            raise WallError('There is a wall there')

    def _get_maze_array(self):
        """Return the entire array; useful for certain walking functions"""
        return self._cells

    def start(self):
        return self._cells[0][0]

if __name__ == '__main__':
    maze = Maze()
    
