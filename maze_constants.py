"""
Constant values for the maze program
"""

MAZE_HEIGHT = 601
MAZE_WIDTH = 801

CELL_SIZE = 10
# includes space for walls, so subtract 2

XCELLS = MAZE_WIDTH / CELL_SIZE
YCELLS = MAZE_HEIGHT / CELL_SIZE

# Colors
NULL_FILL = 'black'
PLAN_FILL = 'grey'
OPEN_FILL = 'white'

DIRECTIONS = {'north': 0, 'east': 1, 'west': 2, 'south': 3}