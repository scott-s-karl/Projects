# Steven Karl
# A Star Path Finding Visualization
# 11/1/2021
# ----------------------------------

# Imports
# --------------
import pygame
from queue import PriorityQueue

# Globals
# --------------
# Width of the display
WIDTH = 800

# Window setup
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Path Finding Visualization")

# Colors to be used when solving the path
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
GREY = (127,127,127)
PURPLE = (75,0,130)
TURQUOISE = (64,224,208)
ORANGE = (204,102,0)
BLACK  = (0,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)

# Local Classes
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.color = WHITE
        self.total_rows = total_rows
        self.neighbors = []

    def get_pos(self):
        return(self.row, self.col)
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    def make_open(self):
        self.color = GREEN
    def make_closed(self):
        self.color = RED
    def make_barrier(self):
        self.color = BLACK
    def make_start(self):
        self.color = ORANGE
    def make_end(self):
        self.color = TURQUOISE
    def make_path(self):
        self.color = PURPLE
    def is_open(self):
        return(self.color == GREEN)
    def is_closed(self):
        return(self.color == RED)
    def is_barrier(self):
        return(self.color == BLACK)
    def is_start(self):
        return(self.color == ORANGE)
    def is_end(self):
        return(self.color == TURQUOISE)
    def is_path(self):
        return(self.color == PURPLE)
    def reset(self):
        self.color = WHITE
    def create_neighbors(self, grid):
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col  - 1])
        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])


            
# Local Functions

def distance_estimate(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return(abs(x1-x2) + abs(y1-y2))

def construct_path(start, end, came_from, draw_screen):

    # loop until you reach start
    cur_node = end
    while cur_node != start:
        cur_node = came_from[cur_node]
        cur_node.make_path()

        draw_screen()

    return None

def find_path(draw_screen, grid, start, end):
    # Define the open set to check as a Priority Queue
    count = 0
    open_set = PriorityQueue()
    
    # Add the start node to the open set
    open_set.put((0, count, start))

    # Define the came from dict for the nodes
    came_from = {}
    
    # Set h,g,f score for all nodes and specifically the node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = g_score[start] + distance_estimate(start.get_pos(), end.get_pos())
    
    # Create an open set dictionary to be able to search if something is in the queue cause you can't do that in the priority queue
    open_set_dict = {start}
    
    # While open set is not empty look for path
    while not open_set.empty():
        # Get the cur node off the open set
        cur_node = open_set.get()[2]

        # When you get something from the open_set then remove it from the dict as well
        open_set_dict.remove(cur_node)

        # Check if the node that we got is the end node
        if cur_node == end:
            construct_path(start, end, came_from, draw_screen)
            start.make_start()
            end.make_end()
            return True

        # Loop through the neighbors of cur node
        for neigh_node in cur_node.neighbors:
            temp_g_score = g_score[cur_node] + 1
            if temp_g_score < g_score[neigh_node]:
                g_score[neigh_node] = temp_g_score
                came_from[neigh_node] = cur_node
                f_score[neigh_node] = g_score[neigh_node] + distance_estimate(neigh_node.get_pos(), end.get_pos())

                # Check if the node is already in the open set dictionary
                if neigh_node not in open_set_dict:
                    
                    # Add to the count so that we know 
                    count+=1

                    # Add it to the open set dict so that we know we still need to look at it
                    open_set_dict.add(neigh_node)
                    
                    # Put it in the open set 
                    open_set.put((f_score[neigh_node], count, neigh_node))

                    # Mark it as open because we just put it in the open set to be looked at later
                    neigh_node.make_open()
        
        # Update the display
        draw_screen()

        if cur_node != start:
            cur_node.make_closed()

    return False

def make_grid(width, rows):
    node_width = width // rows
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, node_width, rows)
            grid[i].append(node)

    return(grid)

def draw_grid(win, width, rows):
    # Define the spacing between the gridlines
    gap = width // rows
    
    # Loop through rows
    for i in range(rows):
        # Put in row line
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        # Loop through the columns
        for j in range(rows):
            # Put in the column lines
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw_screen(win, grid, width, rows):
    # Fill the screen as white each time
    win.fill(WHITE)
    
    # Loop through and refresh all the spots
    for row in grid:
        for node in row:
            node.draw(win)
            
    # Draw the grid
    draw_grid(win, width, rows)

    # Update the display
    pygame.display.update()
    
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x,y = pos
    row = x //gap
    col = y //gap

    return row, col
    
            
def main(win, width):
    # Game State
    running = True

    # Start and End Nodes of path
    start = None
    end = None

    ROWS = 50

    # Define the grid
    grid = make_grid(width, ROWS)
    
    # Game Loop
    while(running):
        # Update the screen
        draw_screen(win, grid, width, ROWS)
        
        # Look for events
        for event in pygame.event.get():
            # Check for quit
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:
                row, col = get_clicked_pos(pygame.mouse.get_pos(), ROWS, width)
                node = grid[row][col]

                if not start:
                    node.make_start()
                    start = node
                elif not end and node != start:
                    node.make_end()
                    end = node
                elif node != start and node != end:
                    node.make_barrier()
                    
            elif pygame.mouse.get_pressed()[2]:
                row, col = get_clicked_pos(pygame.mouse.get_pos(), ROWS, width)
                node = grid[row][col]

                node.reset()
                
                if node == start:
                    start = None
                elif node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start != None and end != None:
                    # update the neighbors of the current set
                    for row in grid:
                        for node in row:
                            node.create_neighbors(grid)

                    # Run the path finding algorithm
                    find_path(lambda:draw_screen(win, grid, width, ROWS), grid, start, end)
                    

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(width,ROWS)
                    
    pygame.quit()


# Call Main
main(WIN, WIDTH)
