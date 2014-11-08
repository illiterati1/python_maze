"""
A maze solver that searches for dead ends in the maze and fills them in.
The only thing left at the end should be the solution
Author: Brendan Wilson
"""

from maze_constants import *
import walker_base

FILL_COLOR = 'gray30'

class DeadendFiller(walker_base.ArrayWalker):

    class Node(object):
        __slots__ = 'filled'

        def __init__(self):
            self.filled = False

        def fill(self):
            self.filled = True

    def __init__(self, maze):
        super(DeadendFiller, self).__init__(maze, maze.start(), self.Node())
        self._maze.clean()

    def _find_paths(self, position, direction):
        """Find directions that are unfilled and unblocked"""
        returnList = []
        for path in position.open_paths(direction):
            newPosition = self._maze._move(position, path)
            if not self.read_map(newPosition).filled:
                returnList.append(path)
        return returnList

    def _is_deadend(self, position, direction=None):
        """Position is the cell in question, and direction is the
        direction the cell was entered from"""

        # Do not fill in the start or finish, obviously
        if position is self._maze.start() or position is self._maze.finish():
            return False
        # Cannot fill what's already filled
        if self.read_map(position).filled:
            return False

        return len(self._find_paths(position, direction)) < 2    
        # True if a deadend

    def _fill(self, position):
        """Starting at a deadend position, fill in cells until a junction
        is reached"""
        path = None
        while self._is_deadend(position):
            #raw_input('')
            path = self._find_paths(position, path)[0]
            self.mark_this(position, lambda node: node.fill())
            self.paint(position, FILL_COLOR)
            if path is None:
                break
            position = self._maze._move(position, path)


    def walk(self):
        for y in xrange(YCELLS):
            for x in xrange(XCELLS):
                current = self._maze._get_cell(x, y)
                self._fill(current)
