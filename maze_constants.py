"""
Constant values for the maze program
"""

from sys import setrecursionlimit

DELAY = 5   # milliseconds

CELL_SIZE = 10      # pixels
# includes space for walls, so subtract 2 ultimately

XCELLS = 60
YCELLS = 60
MAZE_HEIGHT = YCELLS * CELL_SIZE + 1
MAZE_WIDTH = XCELLS * CELL_SIZE + 1
setrecursionlimit((XCELLS+1) * (YCELLS+1))

# Colors
NULL_FILL = 'black'
PLAN_FILL = 'grey'
OPEN_FILL = 'white'

# Helpers
DIRECTIONS = ['north', 'east', 'south', 'west']
OPPOSITES = {'north': 'south', 'east': 'west', 'south': 'north', \
             'west': 'east'}

