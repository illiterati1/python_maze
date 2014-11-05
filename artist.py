"""
A class for keeping track of drawing the maze/grid
Author: Brendan Wilson
"""

import Tkinter as Tk
from maze_constants import *

class MazeArtist(object):
    def __init__(self):
        self.tkCells = [[None for y in xrange(YCELLS)] for x in xrange(XCELLS)]
        self.tkWalls = [[None for y in xrange((YCELLS+1)/2)] \
                        for x in xrange((XCELLS+1)/2)]     
                        # Indices will be x/2, y/2, direction
        self.master = Tk.Tk()
        self.mazeCanvas = Tk.Canvas(self.master, \
                                    height=MAZE_HEIGHT, width=MAZE_WIDTH)
        self.mazeCanvas.pack()

    def _is_congruent(self, x, y):
        """This will make a checkerboard pattern for checking cell walls, so
        we aren't drawing the same wall twice"""
        return (x % 2) == (y % 2)

    def add_cell(self, cell):
        """Make a tk object associated with this cell, and then store that 
        in tkCells. Then if the cell coordinates are congruent mod 2, add
        those wall objects to tkWalls"""

        x, y = cell.get_position()
        topLeft = (x * CELL_SIZE + 1, y * CELL_SIZE + 1)
        bottomRight = (topLeft[0] + CELL_SIZE - 2, topLeft[1] + CELL_SIZE - 2)

    def paint_cell(self, cell, color):
        """Takes a cell object and a color to paint it. Does not update walls.
        Color must be something that Tkinter will recognize."""


if __name__ == '__main__':
	artist = MazeArtist()
	Tk.mainloop()