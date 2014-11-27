"""
The class file for the maze, as well as the cells within the maze.
Author: Brendan Wilson
"""

import time
import Tkinter as Tk
from maze_constants import *
from maze_pieces import Hall, Cell
import wilson
import depth_walker
import breadth_walker

class Maze(Tk.Canvas):

    def __init__(self, frame):
        self._frame = frame
        self._cells = [[Cell(x, y) for y in xrange(YCELLS)] \
                       for x in xrange(XCELLS)]
        for x in xrange(XCELLS-1):
            for y in xrange(YCELLS):
                self._link(self._cells[x][y], 'east', self._cells[x+1][y])
        for x in xrange(XCELLS):
            for y in xrange(YCELLS-1):
                self._link(self._cells[x][y], 'south', self._cells[x][y+1])

        Tk.Canvas.__init__(self, self._frame, height=MAZE_HEIGHT, \
                           width=MAZE_WIDTH, background='black', \
                           highlightthickness=0)
        self.pack()

        for column in self._cells:
            for cell in column:
                self._plot_cell(cell)
                if self._is_congruent(cell):
                    self._plot_walls(cell)

        self.lift('corners')

        self._walker = wilson.Wilson(self)
        self._walker.step()
        self._walker = depth_walker.DepthWalker(self)
        self._walker.step()
        self._walker = breadth_walker.BreadthWalker(self)
        self._walker.step()

    def _is_congruent(self, cell):
        """This will make a checkerboard pattern for checking cell walls, so
        we aren't drawing the same wall twice
        """
        x, y = cell.get_position()
        return (x % 2) == (y % 2)

    def _plot_cell(self, cell):
        """Make a rect on the canvas the size of a cell, and set the cell's
        tk id.
        """
        x, y = cell.get_position()
        topLeft = (x * CELL_SIZE + 2, y * CELL_SIZE + 2)
        bottomRight = (topLeft[0] + CELL_SIZE - 2, topLeft[1] + CELL_SIZE - 2)
        cell.set_id(self.create_rectangle(topLeft, bottomRight, \
                                          fill=NULL_FILL, outline=NULL_FILL))

    def _plot_walls(self, cell):
        """Plot the four walls for a cell and set the hall tk ids."""
        x, y = cell.get_position()
        #y = 2 * y + (0 if x % 2 == 0 else 1)
        x = (x * CELL_SIZE) + 1
        y = (y * CELL_SIZE) + 1

        topLeft = (x, y)
        bottomLeft = (x, y + CELL_SIZE)
        topRight = (x + CELL_SIZE, y)
        bottomRight = (x + CELL_SIZE, y + CELL_SIZE)
        corners = [topLeft, topRight, bottomRight, bottomLeft]
        for corner in corners:
            self.create_rectangle(corner, corner, fill=NULL_FILL, \
                                  tag='corners', outline='')

        wallCoords = [(corners[i], corners[(i + 1) % 4]) for i in xrange(4)]
        for direction, pair in zip(DIRECTIONS, wallCoords):
            hall = cell.get_hall(direction)
            if hall is not None:
                hall.set_id(self.create_line(pair, fill=NULL_FILL))

    def _link(self, cellA, direction, cellB):
        """Build a hallway between cellA and cellB. Direction is A -> B."""
        hall = Hall(cellA, cellB)
        cellA.add_hall(direction, hall)
        cellB.add_hall(OPPOSITES[direction], hall)

    def get_cell(self, x, y):
        """Returns the cell at position x, y.
        x and y are in terms of cell numbers, not pixels"""
        return self._cells[x][y]

    def get_maze_array(self):
        """Return the entire array; useful for certain walking functions"""
        return self._cells

    def clean(self):
        """Return every cell to a default color"""
        for col in self._cells:
            for cell in col:
                self.paint(cell, OPEN_FILL)
        self.update_idletasks()

    def paint(self, cell, color):
        """Takes a cell object and a color to paint it.
        Color must be something that Tkinter will recognize."""
        x, y = cell.get_position()
        self.itemconfigure(cell.get_id(), fill=color, outline=color)

        # Paint the walls
        for hall in cell.get_halls():
            if hall.is_open():  # The wall is down
                fillColor = color
            else:
                fillColor = NULL_FILL
            self.itemconfigure(hall.get_id(), fill=fillColor)

    def start(self):
        return self._cells[0][0]

    def finish(self):
        return self._cells[XCELLS-1][YCELLS-1]

if __name__ == '__main__':
    m = Maze(Tk.Tk())
    Tk.mainloop()