"""
Depth first recursion solver

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

import random
import walker_base
from maze_constants import *

SEARCH_COLOR = 'light blue'
FOUND_COLOR = 'red'
VISITED_COLOR = 'gray70'

class DepthWalker(walker_base.WalkerBase):

    class Node(object):

        __slots__ = 'parent', 'visited'

        def __init__(self):
            self.parent = None
            self.visited = False

    def __init__(self, maze):
        super(DepthWalker, self).__init__(maze, maze.start(), self.Node())
        self._maze.clean()
        self._stack = [self._cell]

    def step(self):
        current = self._stack[-1]
        self.paint(current, SEARCH_COLOR)
        self.read_map(current).visited = True

        if current is self._maze.finish():
            self._isDone = True
            while current is not None:
                self.paint(current, FOUND_COLOR)
                current = self.read_map(current).parent
            return

        paths = current.get_paths(last=self.read_map(current).parent)
        paths = filter((lambda c: self.read_map(c).visited is False), paths)
        random.shuffle(paths)   # Make the path selection random

        if len(paths) == 0:
            # We've found a deadend essentially
            self.paint(current, VISITED_COLOR)
            self._stack.pop()
            return

        for cell in paths:
            self.read_map(cell).parent = current
            self._stack.append(cell)
