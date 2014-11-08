"""
Constant values for the maze program
"""

MAZE_HEIGHT = 801
MAZE_WIDTH = 801

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
RUSH_WILSON = False