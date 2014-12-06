"""Bits that make the maze object work. Not meant to be used by anything
but the maze class.

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

from random import choice

class Piece(object):
    """A base class for the other objects in the maze"""

    __slots__ = '_tkID'

    def set_id(self, ID):
        """Set the Tkinter ID number for the cell"""
        self._tkID = ID

    def get_id(self):
        """Return the tk id number"""
        return self._tkID

class Hall(Piece):
    """An object to connect the cells in the maze together.
    Note: As implemented, you need to instantiate the cells first."""

    __slots__ = '_open', '_cellA', '_cellB',

    def __init__(self, cellA, cellB, isOpen=False):
        # Setting a node to None indicates that there's a permanent wall
        self._cellA = cellA
        self._cellB = cellB
        self._open = isOpen
        self._tkID = None

    def cells(self):
        """Return both ends of the hallway"""
        return [self._cellA, self._cellB]

    def opposite(self, cell, checkWall=True):
        """Get the cell at the other end of the 'hall'.
        Returns None if there is no connection.
        """
        if cell is self._cellA:
            returnCell = self._cellB
        elif cell is self._cellB:
            returnCell = self._cellA
        else:
            raise MazeError('Hall does not refer to this cell')

        if checkWall and not self._open:
            return None
        else:
            return returnCell

    def open_wall(self):
        self._open = True

    def close_wall(self):
        self._open = False

    def is_open(self):
        return self._open

class Cell(Piece):
    """north, east, south, and west will be references to other Cells.
    This class will probably just be passed in to the drawing
    function to deal with displaying the maze."""

    __slots__ = '_paths', '_xLoc', '_yLoc'

    def __init__(self, x, y, north=None, east=None, south=None, west=None):
        self._xLoc = x  # x and y are cell numbers, not pixel numbers
        self._yLoc = y
        self._paths = {'north': north, 'east': east, \
                       'south': south, 'west': west}
        self._tkID = None

    def __str__(self):
        return str(self.get_position())

    def count_halls(self):
        """Return an integer value of open paths from the cell. Basically
        the degree.
        """
        vals = map(lambda h: h.is_open(), \
                   filter(lambda h: h is not None, self._paths.values()))
        return vals.count(True)

    def add_hall(self, direction, hall):
        """Add a hall object the paths dict"""
        self._paths[direction] = hall

    def get_hall(self, direction):
        """Return the hall object itself. Not normally used by anything
        but the maze class.
        """
        return self._paths[direction]

    def get_halls(self):
        """Return every hall object that isn't None"""
        return filter(lambda h: h is not None, self._paths.values())

    def open_wall(self, direction):
        """direction must be 'north', 'east', etc."""
        self._paths[direction].open_wall()

    def build_wall(self, direction):
        self._paths[direction].close_wall()

    def is_open(self, direction):
        """Checks whether the given direction is open"""
        return self._paths[direction].is_open()

    def get_position(self):
        """Return the x, y position of the cell as a tuple"""
        return self._xLoc, self._yLoc

    def get_links(self):
        """Returns the entire direction dict"""
        return self._paths

    def get_paths(self, last=None, checkWalls=True, returnOpen=True):
        """Returns the cells that are connected to this cell and are open.
        last is a cell; it will be omitted. checkWalls will do just that. 
        If it's false, only boundary walls will not return.
        """
        paths = []
        for hall in self.get_halls():
            opposite = hall.opposite(self, False)
            if (not checkWalls or hall.is_open() == returnOpen) and \
            opposite is not last:
                paths.append(opposite)
        return paths

    def random_path(self, last=None, checkWalls=True, returnOpen=True):
        """Return the cell in a random direction."""
        paths = self.get_paths(last, checkWalls, returnOpen)
        return choice(paths)

    def move(self, direction, checkWalls=True):
        """Return the cell in the direction indicated, or None if 
        there is a wall.
        """
        return self._paths[direction].opposite(self, checkWalls)

    def open_by_cells(self, otherCell):
        """Opens the wall given only the two cell values"""
        for hall in self.get_halls():
            if otherCell is hall.opposite(self, False):
                hall.open_wall()
                return
        print self, otherCell
        raise MazeError("These two cells don't touch")

class MazeError(Exception):
    pass

if __name__ == '__main__':
    a = Cell(0, 0)
    b = Cell(1, 0)
    h = Hall(a, b, True)
    a.add_hall('east', h)
    b.add_hall('west', h)
    print a.get_halls()
    print b.get_halls()