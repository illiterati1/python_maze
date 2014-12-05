"""
Constant values for the maze program
"""

from sys import setrecursionlimit

DELAY = 5

# Suggest that these be equal to 1 mod the CELL_SIZE
MAZE_HEIGHT = 602
MAZE_WIDTH = 602

CELL_SIZE = 10
# includes space for walls, so subtract 2 ultimately

XCELLS = MAZE_WIDTH / CELL_SIZE
YCELLS = MAZE_HEIGHT / CELL_SIZE
setrecursionlimit((XCELLS+1) * (YCELLS+1))

# Colors
NULL_FILL = 'black'
PLAN_FILL = 'grey'
OPEN_FILL = 'white'

# Helpers
DIRECTIONS = ['north', 'east', 'south', 'west']
OPPOSITES = {'north': 'south', 'east': 'west', 'south': 'north', \
             'west': 'east'}

# Flags
## Wilson's algorithm
RUSH_WILSON = True

