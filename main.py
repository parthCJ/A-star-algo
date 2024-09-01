import pygame  # Import the pygame library for creating the graphical interface
import math  # Import math for mathematical calculations
from queue import PriorityQueue  # Import PriorityQueue to implement the A* algorithm

# Define the width of the window and initialize the display
WIDTH = 650
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")  # Set the window title

# Define RGB color constants
RED = (255, 0, 0)  # For closed nodes
GREEN = (0, 255, 0)  # For open nodes
BLUE = (0, 255, 0)  # Unused, could be used for other purposes
YELLOW = (255, 255, 0)  # Unused, could be used for other purposes
WHITE = (255, 255, 255)  # For empty nodes
BLACK = (0, 0, 0)  # For barriers
PURPLE = (128, 0, 128)  # For the path
ORANGE = (255, 165 ,0)  # For the start node
GREY = (128, 128, 128)  # For the grid lines
TURQUOISE = (64, 224, 208)  # For the end node

# Define a class to represent each spot on the grid
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row  # Row position
        self.col = col  # Column position
        self.x = row * width  # x-coordinate for drawing
        self.y = col * width  # y-coordinate for drawing
        self.color = WHITE  # Default color is white (empty)
        self.neighbors = []  # List to store neighboring spots
        self.width = width  # Width of each spot
        self.total_rows = total_rows  # Total number of rows in the grid

    # Get the position of the spot
    def get_pos(self):
        return self.row, self.col

    # Check if the spot is closed (already evaluated)
    def is_closed(self):
        return self.color == RED

    # Check if the spot is open (in the open set)
    def is_open(self):
        return self.color == GREEN

    # Check if the spot is a barrier
    def is_barrier(self):
        return self.color == BLACK

    # Check if the spot is the start node
    def is_start(self):
        return self.color == ORANGE

    # Check if the spot is the end node
    def is_end(self):
        return self.color == TURQUOISE

    # Reset the spot to its default state
    def reset(self):
        self.color = WHITE

    # Mark the spot as the start node
    def make_start(self):
        self.color = ORANGE

    # Mark the spot as closed
    def make_closed(self):
        self.color = RED

    # Mark the spot as open
    def make_open(self):
        self.color = GREEN

    # Mark the spot as a barrier
    def make_barrier(self):
        self.color = BLACK

    # Mark the spot as the end node
    def make_end(self):
        self.color = TURQUOISE

    # Mark the spot as part of the path
    def make_path(self):
        self.color = PURPLE

    # Draw the spot on the window
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # Update the neighbors of the spot (check the four possible directions)
    def update_neighbors(self, grid):
        self.neighbors = []  # Clear existing neighbors

        # Check and add the neighboring spot to the list if it's within bounds and not a barrier
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    # Define the less-than operator (needed for the PriorityQueue)
    def __lt__(self, other):
        return False

# Heuristic function for A* (Manhattan distance)
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Function to reconstruct the path once the end node is reached
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()  # Redraw the grid with the updated path

# Implementation of the A* algorithm
def algorithm(draw, grid, start, end):
    count = 0  # Counter to keep track of when the node was added
    open_set = PriorityQueue()  # Priority queue to store the open set
    open_set.put((0, count, start))  # Add the start node to the open set
    came_from = {}  # Dictionary to store the path
    g_score = {spot: float("inf") for row in grid for spot in row}  # Initialize g_scores
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}  # Initialize f_scores
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}  # Set to keep track of nodes in the open set

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  # Get the node with the lowest f_score
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True  # Path found

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False  # Path not found

# Function to create the grid of spots
def make_grid(rows, width):
    grid = []
    gap = width // rows  # Calculate the width of each spot
    for i in range(rows):
        grid.append([])  # Add a new row
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)  # Add a new spot to the row

    return grid

# Function to draw the grid lines
def draw_grid(win, rows, width):
    gap = width // rows  # Calculate the distance between grid lines
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))  # Horizontal lines
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))  # Vertical lines

# Function to draw the grid and spots on the window
def draw(win, grid, rows, width):
    win.fill(WHITE)  # Fill the window with white

    for row in grid:
        for spot in row:
            spot.draw(win)  # Draw each spot

    draw_grid(win, rows, width)
    pygame.display.update()  # Update the display

# Function to get the position of the mouse click in the grid
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

# Main function to run the program
def main(win, width):
    ROWS = 50  # Define the number of rows in the grid
    grid = make_grid(ROWS, width)  # Create the grid

    start = None  # Initialize the start node
    end = None  # Initialize the end node

    run = True
    while run:
        draw(win, grid, ROWS, width)  # Draw the grid and spots
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Quit the program

            if pygame.mouse.get_pressed()[0]:  # LEFT mouse button click
                pos = pygame.mouse.get_pos()
                                row, col = get_clicked_pos(pos, ROWS, width)  # Get the row and column where the mouse was clicked
                spot = grid[row][col]  # Get the spot object at the clicked position

                # Set the start node if it's not already set, and the clicked spot is not the end node
                if not start and spot != end:
                    start = spot
                    start.make_start()

                # Set the end node if it's not already set, and the clicked spot is not the start node
                elif not end and spot != start:
                    end = spot
                    end.make_end()

                # If the clicked spot is neither the start nor the end, make it a barrier
                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT mouse button click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)  # Get the clicked position
                spot = grid[row][col]  # Get the spot object at the clicked position
                spot.reset()  # Reset the spot to its default state (white)

                # If the reset spot was the start node, clear the start
                if spot == start:
                    start = None

                # If the reset spot was the end node, clear the end
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                # Start the A* algorithm when the spacebar is pressed
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)  # Update neighbors for each spot

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)  # Run the algorithm

                # Clear the grid when the "C" key is pressed
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)  # Reset the grid

    pygame.quit()  # Quit the game

# Run the main function
main(WIN, WIDTH)

