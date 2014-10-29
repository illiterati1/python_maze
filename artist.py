"""
A class for keeping track of drawing the maze/grid
Author: Brendan Wilson
"""

import Tkinter as Tk
from maze_constants import *

class MazeArtist(object):
    def __init__(self):
        self.master = Tk.Tk()
        self.mazeCanvas = Tk.Canvas(self.master, height=MAZE_HEIGHT, width=MAZE_WIDTH)
        self.mazeCanvas.pack()
        self.mazeCanvas.create_rectangle(0, 0, MAZE_WIDTH, MAZE_HEIGHT, fill='dark grey')

if __name__ == '__main__':
	artist = MazeArtist()
	artist.mainloop()