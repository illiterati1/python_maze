"""
Constant values for the maze program
"""

# Suggest that these be equal to 1 mod the CELL_SIZE
MAZE_HEIGHT = 401
MAZE_WIDTH = 401

CELL_SIZE = 10
# includes space for walls, so subtract 2

XCELLS = MAZE_WIDTH / CELL_SIZE
YCELLS = MAZE_HEIGHT / CELL_SIZE

# Colors
NULL_FILL = 'black'
PLAN_FILL = 'grey'
OPEN_FILL = 'white'

# Helpers
DIRECTIONS = {'north': 0, 'east': 1, 'south': 2, 'west': 3}
OPPOSITES = {'north': 'south', 'east': 'west', 'south': 'north', \
             'west': 'east'}

# Flags
## Wilson's algorithm
RUSH_WILSON = True
WILSON_SPEED = 10    # A parameter that controls how fast the wilson walker
# runs. Note: if RUSH_WILSON is True, SPEED is ignored