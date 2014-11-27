"""
A maze solver that searches for dead ends in the maze and fills them in.
The only thing left at the end should be the solution
Author: Brendan Wilson
"""

from maze_constants import *
import walker_base

FILL_COLOR = 'gray30'

class DeadendFiller(walker_base.WalkerBase):

    class Node(object):
        __slots__ = 'filled'

        def __init__(self):
            self.filled = False

    def __init__(self, maze):
        super(DeadendFiller, self).__init__(maze, maze.start(), self.Node())
        self._maze.clean()

    def _find_paths(self, current):
        """Find directions that are unfilled and unwalled"""
        return filter(lambda c: not self.read_map(c).filled, \
                      current.get_paths())

    def _is_deadend(self, current):
        """Position is the cell in question, and direction is the
        direction the cell was entered from"""

        if current in [self._maze.start(), self._maze.finish()] or \
        self.read_map(current).filled:
            return False

        return len(self._find_paths(current)) < 2    
        # True if a deadend

    def _fill(self, cell):
        """Starting at a deadend position, fill in cells until a junction
        is reached"""
        while self._is_deadend(cell):
            next = self._find_paths(cell)[0]
            self.read_map(cell).filled = True
            self.paint(cell, FILL_COLOR)
            self._maze.update_idletasks()
            cell = next
        
    def step(self):
        for y in xrange(YCELLS):
            for x in xrange(XCELLS):
                current = self._maze.get_cell(x, y)
                self._fill(current)

# TODO: Make a blind alley filler subclass