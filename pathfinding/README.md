# Path Finding Visualization Tool

This is Path Finding visualization Tool. It shows runtime working(exploring) of pathfinding algorithms.
When the search reaches the end, shortest(not for DFS) path is highlighted from the start to end.

## Path Finding Algorithms used:
1. A* (star)
2. 
3. BFS
4. Dijkstra's algorithm

## How to run

You will need pygame and pqdict installed on your system. I suggest you to do that in a virtual environment.
Using pip,
pygame: $ pip install pygame
pqdict: $ pip install pqdict

Note: pqdict dict is required as it provides a indexed priority queue, which is used in dijkstra's algorithm for better efficiency.

All of the code is written in a single file called 'astar.py'. Download the file and simply execute the code.

After running the code, a pygame window will open with an interactive 2D grid. This grid is made of blocks, I call them cells.

### GRID SETUP:
To add START/END/OBSTACLE cells, use left-mouse button. The placement order of cells is START >>> END >>> OBSTACLES.
This means on an empty grid, your first left-mouse click on a cell will make it the START. The next click on a different cell will make it the END. And then you can make as many cell as obstacles.
You don't need to click every time you lay obstacles, simply press down the left-mouse button and drag.
To remove START/END/OBSTACLE cells, use right-mouse button. Please note, the placement order remains same, that is if your remove your START, the next left-click will place your START.

Color Coding:
1. START:     orange
2. END:       turquoise(blue)
3. OBSTACLE:  black

### PATH EXPLORATION
Now that you have your grid setup ready, that is the START cell, END cell, and OBSTACLE cells if any.

There are four algorithms, you need to choose one of them.

Enter(press on keyborad):
1. 'a' to run A* algorithm.
2. 'd' to run DFS algorithm.
3. 'b' to run BFS algorithm.
4. 'k' to run dijkstra's algorithm.
5. 'c' to clear paths/explored areas.
6. 'r' to clear the grid setup. (reset whole grid)

Now, sit back and see the algorithm explore your grid setup to find a shortest path between START and END cell.
Once it reaches there, a path will be created from the END to start in purple color.
