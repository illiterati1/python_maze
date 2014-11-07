"""
A class for keeping track of drawing the maze/grid
Author: Brendan Wilson
"""

import Tkinter as Tk
from maze_constants import *

class MazeArtist(object):
    def __init__(self):
        self.master = Tk.Tk()
        self.mazeCanvas = Tk.Canvas(self.master, \
                                    height=MAZE_HEIGHT, width=MAZE_WIDTH)
        self.mazeCanvas.pack()

        #self.mazeCanvas.create_rectangle(1, 1, MAZE_WIDTH, MAZE_HEIGHT, outline='black')
        """self.tkCells = [[self._plot_cell(x, y) for y in xrange(YCELLS)] \
                        for x in xrange(XCELLS)]"""

        self.tkWalls = [[self._plot_walls(x, y) \
                         for y in xrange(self._transform(YCELLS))] \
                        for x in xrange(XCELLS)]

        """
        # TODO: This next bit needs refactoring, but is low priority if it works
        self.tkWalls = [[None for y in xrange(self._transform(YCELLS))] for x in xrange(XCELLS)]
        for x in xrange(XCELLS):
            for y in xrange(self._transform(YCELLS)):
                self.tkWalls[x][y] = self._plot_walls(x, y)
                        # Indices will be x/2, y/2, direction
        """
    
    def _transform(self, n):
        return (n + 1) / 2

    def _is_congruent(self, x, y):
        """This will make a checkerboard pattern for checking cell walls, so
        we aren't drawing the same wall twice"""
        return (x % 2) == (y % 2)

    def _plot_cell(self, x, y):
        """Make a rect on the canvas the size of a cell, and return the Tk 
        item number associated with it."""
        topLeft = (x * CELL_SIZE + 1, y * CELL_SIZE + 1)
        bottomRight = (topLeft[0] + CELL_SIZE - 2, topLeft[1] + CELL_SIZE - 2)

        return self.mazeCanvas.create_rectangle(topLeft, bottomRight,\
                                                fill='black', outline="black")

    def _plot_walls(self, x, y):
        """Plot the four walls for a cell and return a list of the Tk IDs in the
        form [north, east, south, west]"""
        print x, y
        y = 2*y + (0 if x % 2 == 0 else 1)
        x = (x * CELL_SIZE) + 1
        y = (y * CELL_SIZE) + 1
        print x, y
        print

        returnList = []
        topLeft = (x, y)
        bottomLeft = (x, y + CELL_SIZE)
        topRight = (x + CELL_SIZE, y)
        bottomRight = (x + CELL_SIZE, y + CELL_SIZE)
        corners = [topLeft, topRight, bottomRight, bottomLeft]
        for i in xrange(4):
            returnList.append(self.mazeCanvas.create_line(corners[i], corners[(i+1)%4]))

    def paint_cell(self, cell, color):
        """Takes a cell object and a color to paint it. Does not update walls.
        Color must be something that Tkinter will recognize."""


if __name__ == '__main__':
    artist = MazeArtist()
    Tk.mainloop()