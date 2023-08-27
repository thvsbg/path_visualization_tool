# Refer README.md to understand how to work with the interactive 2D grid.

import pygame
import math
from queue import PriorityQueue, Queue
from pqdict import pqdict
from collections import deque

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Path Finding Visualization Tool")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
PINK = (255,182,193)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224,208)


# Spot is the individual cell of our grid.
class Spot:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def is_path(self):
        return self.color == PURPLE

    def reset(self):            # This will reset the whole grid.
        self.color = WHITE

    def make_start(self):       # This will create the START.
        self.color = ORANGE

    def make_closed(self):      # This will set visited cells to red(for visuals).
        self.color = RED

    def make_open(self):        # This will set current neighbours which can be visited to green(for visuals).
        self.color = GREEN

    def make_barrier(self):     # This will create obstacles.
        self.color = BLACK
    
    def make_end(self):         # This will create the END.
        self.color = TURQUOISE
    
    def make_path(self):        # This will highlight the path in purpule.
        self.color = PURPLE

    def draw(self, win):        # This function will actually draw those (individual)cells on the grid.
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

# Code for A* (star) algorithm.
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        if current != None:
            current.make_path()
        draw()

def reconstruct_path_dfs(stack, draw):
    while len(stack):
        current = stack.pop()
        current.make_path()
        draw()

def dijkstra(draw, grid, start, end):
    minDistance = pqdict()
    for row in grid:
        for spot in row:
            if spot.is_start():
                minDistance.additem(spot,0)
            elif not spot.is_barrier():
                minDistance.additem(spot,float("inf"))

    parent = {}

    while len(minDistance):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = minDistance.popitem()
        if current[1] == float("inf"):
            return
        if current[0] != start: 
            current[0].make_closed()

        for neighbor in current[0].neighbors:
            if neighbor == end:
                parent[end] = current[0]
                reconstruct_path(parent, end, draw)
                return

            elif not neighbor.is_closed() and neighbor != start:
                neighbor.make_open()
                currentDistance = minDistance[neighbor]
                minDistance.updateitem(neighbor,min(current[1]+1,currentDistance))
                parent[neighbor] = current[0]

        draw()


def bfs(draw, grid, start, end):
    parent = {}
    parent[start] = None
    que = Queue(maxsize = 10000)
    que.put(start)

    while not que.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = que.get()         # Say this is our current node/cell/spot.
        if current != start:
            current.make_closed()
        for neighbor in current.neighbors:
            if neighbor == end:
                parent[end] = current
                reconstruct_path(parent, end, draw)
                return

            if not neighbor.is_open() and not neighbor.is_closed() and neighbor != start:
                neighbor.make_open()
                que.put(neighbor)
                parent[neighbor] = current

        draw()


def dfs(draw, grid, start, end):
    stack = deque()     # Stack of nodes/cells
    stack.append(start)
    found = False

    while len(stack):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack[-1]
        for neighbor in current.neighbors:
            if neighbor == end:
                found = True
                reconstruct_path_dfs(stack, draw)
                break

            if not neighbor.is_open() and not neighbor.is_closed() and neighbor != start and neighbor != end:
                neighbor.make_open()

        if found:
            break;

        if current != start:
            current.make_closed()

        btrack = True
        for neighbor in current.neighbors:
            if neighbor.is_open():
                stack.append(neighbor)
                btrack = False
                break

        if btrack:
            current.color = PINK
            stack.pop()
            draw()
            current.make_closed()

        else:
            draw()


def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i,j,gap,rows)
            grid[i].append(spot)
    
    return grid

# def draw_grid(win, rows, width): #This takes O(N^2) time
#     gap = width // rows
#     for i in range(rows):
#         pygame.draw.line(win, GREY, (0,i * gap),(width, i * gap))
#         for j in range(rows):
#             pygame.draw.line(win, GREY, (j * gap,0), (j * gap, width))

def draw_grid(win, rows, width):  #This takes O(N) time
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY,(0, i * gap),(width, i * gap))
        pygame.draw.line(win, GREY,(i * gap, 0),(i * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap =  width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def neighbours(grid):
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    
    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue
                
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    neighbours(grid)
                    a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and start and end:
                    neighbours(grid)
                    dfs(lambda: draw(win, grid, ROWS, width), grid, start, end)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and start and end:
                    neighbours(grid)
                    bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k and start and end:
                    neighbours(grid)
                    dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    for row in grid:
                        for spot in row:
                            if spot.is_path() or spot.is_closed() or spot.is_open():
                                spot.reset()
                    start.make_start();

                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)