"""
A random mouse class for the maze.

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

from random import choice
from maze_constants import *
from walker_base import WalkerBase

MOUSE_COLOR = 'brown'

class RandomMouse(WalkerBase):

    def __init__(self, maze):
        super(RandomMouse, self).__init__(maze, maze.start())
        self._maze.clean()
        self._last = None
        self._delay = 50

    def step(self):
        if self._cell is self._maze.finish():
            self._isDone = True
            return

        paths = self._cell.get_paths(last=self._last)

        if len(paths) == 0:
            # We've hit a deadend
            self._cell, self._last = self._last, self._cell
        else:
            self._last = self._cell
            self._cell = choice(paths)

        self.paint(self._cell, MOUSE_COLOR)
        self.paint(self._last, OPEN_FILL)