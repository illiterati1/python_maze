"""
A class for keeping track of drawing the maze/grid
Author: Brendan Wilson
"""

import Tkinter as Tk
from maze_constants import *
import maze
import wilson
import depth_walker
import breadth_walker
import deadend_filler

class MazeArtist(object):
    def __init__(self):
        self.master = Tk.Tk()
        self.mazeCanvas = Tk.Canvas(self.master, \
                                    height=MAZE_HEIGHT, width=MAZE_WIDTH)
        self.mazeCanvas.pack()

        self.mazeCanvas.create_rectangle(1, 1, MAZE_WIDTH, MAZE_HEIGHT, \
                                         outline='black')

        self.tkCells = [[self._plot_cell(x, y) for y in xrange(YCELLS)] \
                        for x in xrange(XCELLS)]

        self.tkWalls = [[self._plot_walls(x, y) \
                         for y in xrange(YCELLS)] \
                        for x in xrange(XCELLS)]
        self.mazeCanvas.lift('corners')
        self.mazeCanvas.update_idletasks()
    
    def _transform(self, n):
        return n / 2

    def _is_congruent(self, x, y):
        """This will make a checkerboard pattern for checking cell walls, so
        we aren't drawing the same wall twice"""
        return (x % 2) == (y % 2)

    def _plot_cell(self, x, y):
        """Make a rect on the canvas the size of a cell, and return the Tk 
        item number associated with it."""
        topLeft = (x * CELL_SIZE + 2, y * CELL_SIZE + 2)
        bottomRight = (topLeft[0] + CELL_SIZE - 2, topLeft[1] + CELL_SIZE - 2)

        return self.mazeCanvas.create_rectangle(topLeft, bottomRight,\
                                                fill=NULL_FILL, outline=NULL_FILL)

    def _plot_walls(self, x, y):
        """Plot the four walls for a cell and return a list of the Tk IDs in the
        form [north, east, south, west]"""
        y = 2 * y + (0 if x % 2 == 0 else 1)
        x = (x * CELL_SIZE) + 1
        y = (y * CELL_SIZE) + 1

        returnList = []
        topLeft = (x, y)
        bottomLeft = (x, y + CELL_SIZE)
        topRight = (x + CELL_SIZE, y)
        bottomRight = (x + CELL_SIZE, y + CELL_SIZE)
        corners = [topLeft, topRight, bottomRight, bottomLeft]
        for i in xrange(4):
            self.mazeCanvas.create_rectangle(corners[i], corners[i], fill=NULL_FILL, tag='corners', outline='')
            returnList.append(self.mazeCanvas.create_line(corners[i], corners[(i+1)%4], fill=NULL_FILL))
        return returnList

    def paint_cell(self, cell, color, redraw=True, changeWalls=True):
        """Takes a cell object and a color to paint it.
        Color must be something that Tkinter will recognize."""
        x, y = cell.get_position()
        self.mazeCanvas.itemconfigure(self.tkCells[x][y], fill=color, outline=color)

        if changeWalls and self._is_congruent(x, y):
            y = self._transform(y)
            for direction, index in DIRECTIONS.items():
                if cell.get_links()[direction]:  # The wall is down
                    fillColor = color
                else:
                    fillColor = NULL_FILL
                self.mazeCanvas.itemconfigure(self.tkWalls[x][y][index], fill=fillColor)

        if redraw:
            self.mazeCanvas.update_idletasks()

if __name__ == '__main__':
    artist = MazeArtist()
    maze = maze.Maze(artist)
    walker = wilson.LoopyWilson(maze)
    walker.build_maze()

    walker = depth_walker.DepthWalker(maze)
    walker.walk()

    walker = breadth_walker.BreadthWalker(maze)
    walker.walk()
    
    walker = deadend_filler.DeadendFiller(maze)
    walker.walk()

    Tk.mainloop()

