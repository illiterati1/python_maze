#!/usr/bin/python

"""
The class file for the maze, as well as the cells within the maze.

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

from textwrap import fill
import Tkinter as Tk
from maze_constants import *
from maze_pieces import Hall, Cell
from wilson import Wilson
from depth_walker import DepthWalker
from breadth_walker import BreadthWalker
from deadend_filler import DeadendFiller
from tremaux import Tremaux
from mouse import RandomMouse

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

        for cell, color in zip([self.start(), self.finish()], DOT_COLORS):
            self.create_oval(*self._cell_bounds(cell), fill=color, \
                               tag='dots', outline='')

        self.lift('corners')
        self.lower('dots')
        self.update_idletasks()
        self.prompt_build()

    def _run(self):
        if not self._walker.is_done():
            self._walker.step()
            self.after(self._walker.delay(), self._run)
        else:
            self.lift('dots')
            self.prompt()

    def prompt_build(self):
        """Get user input before the maze has been built"""
        factor = raw_input("Enter loop factor (0: No loops; 100: All loops): ")
        print "How much of the maze building would you like to see?"
        print "1: Show me everything"
        print "2: Just give me the broad strokes"
        print "3: I don't have all day. Mach schnell!"
        try:
            speed = int(raw_input(">> "))
        except ValueError:
            print "Since you can't type, I can only assume you're in a hurry."
            speed = 3
        print 'Building...'
        self._walker = Wilson(self, float(factor) / 100.0, speed)
        self.after(self._walker.delay(), self._run)

    def prompt(self):
        """Get user input after the maze has been built"""
        
        classes = {'d': DepthWalker, 'b': BreadthWalker, 'f': DeadendFiller, \
                   't': Tremaux, 'm': RandomMouse}
        while True:
            print "Choose maze solving algorithm"
            print "(D)epth first search"
            print "(B)readth first search"
            print "Deadend (f)iller"
            print "(T)remaux's algorithm"
            print "Random (m)ouse"
            print "(R)ebuild maze"
            print "(Q)uit"
            choice = raw_input(">> ").strip().lower()

            if choice == 'q':
                raise SystemExit
            elif choice == 'r':
                self.rebuild()
                return

            try:
                walkClass = classes[choice]
            except KeyError:
                continue

            break

        self._walker = walkClass(self)
        self.after(self._walker.delay(), self._run)

    def rebuild(self):
        """Clean and rebuild the maze"""
        self.lower('dots')
        for column in self._cells:
            for cell in column:
                for hall in cell.get_halls():
                    hall.close_wall()
                self.paint(cell, NULL_FILL)
        self.update_idletasks()
        self.prompt_build()

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
        topLeft, bottomRight = self._cell_bounds(cell)
        cell.set_id(self.create_rectangle(topLeft, bottomRight, \
                                          fill=NULL_FILL, outline=NULL_FILL))

    def _cell_bounds(self, cell):
        """Return the a tuple of the top left and bottom right corners of the
        cell object suitable for drawing.
        """
        x, y = cell.get_position()
        topLeft = (x * CELL_SIZE + 1, y * CELL_SIZE + 1)
        bottomRight = (topLeft[0] + CELL_SIZE - 2, topLeft[1] + CELL_SIZE - 2)
        return topLeft, bottomRight

    def _plot_walls(self, cell):
        """Plot the four walls for a cell and set the hall tk ids."""
        x, y = cell.get_position()
        x = (x * CELL_SIZE)
        y = (y * CELL_SIZE)

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

    def paint(self, cell, color, paintWalls=True):
        """Takes a cell object and a color to paint it.
        Color must be something that Tkinter will recognize."""
        self.itemconfigure(cell.get_id(), fill=color, outline=color)

        # Paint the walls
        if paintWalls:
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
    print "python_maze  Copyright (C) 2014  Brendan Wilson"
    print "This program comes with ABSOLUTELY NO WARRANTY."
    print fill("This is free software, and you are welcome to " + \
                        "redistribute it under certain conditions.")
    print "See http://www.gnu.org/copyleft/gpl.html for more details."
    root = Tk.Tk()
    root.title('Maze')
    maze = Maze(root)
    root.mainloop()