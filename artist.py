"""
A class for keeping track of drawing the maze/grid
Author: Brendan Wilson
"""

import Tkinter as Tk
from maze_constants import *


class MazeArtist(Tk.Canvas):
    def __init__(self):
        self.maze = maze.Maze(self)
        self.master = Tk.Tk()
        

        self.run()
    
    def _transform(self, n):
        return n / 2

    

    

    def paint_cell(self, cell, color, redraw=True, changeWalls=True):
    

    def run(self):
        walker = wilson.LoopyWilson(self.maze)
        walker.build_maze()
        raw_input()

        walker = depth_walker.DepthWalker(self.maze)
        walker.walk()
        raw_input()

        walker = breadth_walker.BreadthWalker(self.maze)
        walker.walk()
        raw_input()
        
        walker = deadend_filler.DeadendFiller(self.maze)
        walker.walk()
        raw_input()

if __name__ == '__main__':
    artist = MazeArtist()
    artist.master.mainloop()

