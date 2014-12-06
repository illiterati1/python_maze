"""
A maze solver that searches for dead ends in the maze and fills them in.
The only thing left at the end should be the solution

Copyright (C) 2014 Brendan Wilson
brendan.x.wilson@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
        self.x = 0
        self.y = 0

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
            cell = next
        
    def step(self):
        if self.x == XCELLS:
            self.x = 0
            self.y += 1
        if self.y == YCELLS:
            self._isDone = True
        else:
            current = self._maze.get_cell(self.x, self.y)
            self._fill(current)
            self.x += 1

# TODO: Make a blind alley filler subclass