python_maze
===========
maze.py - A maze generation and solving program
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

This is a maze generation and solving project built using Python 2.7.6. To run it, I would recommend opening a terminal in the folder containing the program files, and calling

    python maze.py

This will open the maze window, however at this point all interaction is still done using the terminal window, so make sure to have that visible. The program will ask you how 'loopy' you want the maze, or in technical terms, how many cycles the graph contains. Enter a number from 0 to 100 to set this (0 will generate no cycles, 100 will be almost nothing but.) 

Then the program will ask how much detail you want to see while building the maze. The slowest speed will show every detail in building the maze, and may be very slow indeed. The fastest speed should generate the maze within a few seconds, although because of randomness there is variability in that time. And of course the middle speed will be somewhere in between. See the algorithms section for more details.

Once the maze is finished, you will be given options for maze completion algorithms to run. You will have a choice between depth-first search, breadth-first search, deadend filler, Tremaux's algorithm, random mouse, rebuilding the maze, and quitting the program. 

NOTE: Random mouse may take a very, very long time to complete. As of now, there is no way to stop a solver in progress other than quitting, so be careful about selecting this. It's mostly a novelty.

You may also quit at any time by closing the maze window. The maze solvers will proceed from the top left corner of the maze to the bottom right. These points will be indicated by a green and red dot respectively. Again, see the algorithm section if you want to know the gory details.

If you want to change the size of the maze, you will have to be a bit adventurous and modify the maze_constants.py file. XCELLS and YCELLS determine how tall/wide the maze is. CELL_SIZE can be changed as well, should you want bigger or smaller squares. I take no responsibility for results obtained through fiddling with these.


Algorithms:

Wilson's algorithm

This is the algorithm that generates the maze. It's not named after me, by the way; that's just a fun coincidence. It starts with all cells in the maze closed and walled off from every other cell, except for the starting cell, which is marked as open. Starting at a closed cell, the algorithm will randomly walk the maze-space until it runs into a cell that is marked as open. All the cells on this path are then opened, and the algorithm starts this process again at the next closed cell it finds. While performing the random walk, if the walker runs back into the random path, it will clip off the portion of the path past this point. This keeps cycles from appearing in the maze. If you run the algorithm at the slowest speed, the open cells will appear as white, and the random path will appear as gray. If you choose the medium speed, only the open cells will be shown (the random walker is very slow when drawn). At the fastest speed, no drawing will be performed until the maze is complete.
The algorithm is complete when every cell is open. If you've selected a non-zero loop factor, the program will then search through the maze for any deadends. When a deadend is found, the loop factor will be compared to a random number generator to determine whether to open the deadend.

Depth-first search

This is a very common method for determining a solution to a graph. It is not always very efficient or quick, but it will always find a solution to the maze if one exists. It is not guaranteed to find the shortest solution in a cyclic maze. Since an acyclic maze contains only one solution, by necessity it will find the shortest solution.
It works by a recursive process. Starting from a cell, it checks if the cell is the finish. If not, then it repeats this process on every cell connected to the first cell that hasn't already been visited. This is technically accomplished through the use of a stack. The program looks at the cell on the top of the stack, and if it's not the finish, it adds all the 'children' of this cell onto the top of the stack, and repeats. If it runs into a deadend, cells are removed from the stack until it finds one that hasn't been visited.
The current path the algorithm is considering will be shown as light blue, and any cell that has been visited but is not on the path will be colored gray. When complete, the solution will be shown as red.

Breadth-first search

In contrast to the depth-first search, this is guaranteed to find the shortest path in any maze. The intuitive way to think about it is water being poured into the maze over the starting cell. This water will spread out evenly in all directions, and as soon as the water hits the finish, the algorithm has found the shortest path.
Where depth-first search uses a stack to keep track of cells, breadth-first uses a queue. The program will pull a cell from the front of the queue, check if it's the finish, and if not, add the unvisited children of this cell to the back of the queue. In this way, 'layers' of cells are checked that are all equidistant from the start cell. As each cell is added, a pointer to the cell 'upstream' of it is noted. This lets the algorithm determine the route back to the start from the finish by following these pointers backwards.
The layers of cells will cycle through a grayscale color scheme to indicate the current distance from the start. The structure of acyclic versus cyclic mazes can be seen very well if this is performed on each. When the shortest path is found, it will be marked in red.

Deadend filler

This algorithm works by finding deadends in the maze and filling in every cell in the deadend until a junction is reached. In an acyclic maze, this will show only the solution to the maze. If there are cycles in the maze, there may be cycles in the solution as well, but there may also be 'nooses', which appear to be deadends but have a cycle at the far end. This is one shortcoming of this algorithm. In a very cyclic maze, it may not appear to do anything at all. All it guarantees is that you can walk from the start to the finish without ever performing a 180 degree turn.

Tremaux's algorithm

This algorithm will actually look very similar to a depth-first search, because essentially, that's what it is. The main difference is that, in contrast to depth-first search, it is performable by a human in the maze. All they would need is a bucket of paint or some other way to mark cells. In fact, the algorithm was invented in the 19th century, presumably on some early version of DOS. It operates on a few simple rules.
Rule 1: Walk until you hit a junction. If it's a junction you haven't visited before, choose a path at random and mark it somehow.
Rule 2: If you hit a junction you have visited before but are not backtracking (you could tell from the marks you made), treat it like a deadend and turn around.
Rule 3: If you've backtracked to a junction, go down any paths you have not visited before. If there are none, keep backtracking.
When you reach the finish, any cells you've only marked once will indicate the path back to the start. In the program, cells visited once will be red, and cells visited twice will be gray.

Random mouse

This is just here for completeness. It is probably the most naive (read: dumb) way to solve a maze. The 'mouse' walks down a path until it hits a junction, and then chooses a path other than the one it just came down. That's it. As you might imagine, this can take a very long time to solve a maze, and there will be no indication how to get back to the start once it has finished. In fact, there is really no guarantee that this will ever solve a maze before the heat death of the universe. If you really want to see it work, I'd recommend doing it on a very small maze.


References:

As always, here are the wikis, though they are not always easy to read:
http://en.wikipedia.org/wiki/Maze_solving_algorithm
http://en.wikipedia.org/wiki/Maze_generation_algorithm

This is an excellent resource for every algorithm I've mentioned:
http://www.astrolog.org/labyrnth/algrithm.htm

Here is a thorough explanation of Tremaux's algorithm:
http://blog.jamisbuck.org/2014/05/12/tremauxs-algorithm.html

And here is a great breakdown of Wilson's algorithm:
http://bl.ocks.org/mbostock/11357811
