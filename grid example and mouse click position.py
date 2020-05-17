import pygame
import numpy as np

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# This sets the WIDTH and HEIGHT of each grid location
NumRow = 20
NumCol = 20

WIDTH = 20
HEIGHT = 20

MARGIN = 5  # This sets the margin between each cell

WindowHeight = (2 * MARGIN) + (HEIGHT * NumRow) + ((NumRow - 1) * MARGIN)
WindowWidth = (2 * MARGIN) + (WIDTH*NumCol) + ((NumCol - 1)*MARGIN)

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(NumRow):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(NumCol):
        grid[row].append(0)  # Append a cell

# (Remember rows and column numbers start at zero.)
grid[1][5] = 1
grid[3][5] = 2
grid[2][5] = 3
print(grid)
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [WindowWidth, WindowHeight]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Array Backed Grid")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = np.clip(
                int((pos[0]-0.5*MARGIN) // (WIDTH+MARGIN)), 0, NumCol-1)
            row = np.clip(int((pos[1]-0.5*MARGIN) // (HEIGHT+MARGIN)), 0, NumRow-1)

            if pygame.mouse.get_pressed()[0]:
                grid[row][column] = 1
            elif pygame.mouse.get_pressed()[1]:
                grid[row][column] = 2
            elif pygame.mouse.get_pressed()[2]:
                grid[row][column] = 3
            print(pygame.mouse.get_pressed(), pos,
                  "Grid coordinates: ", row, column)

    # Set the screen background
    screen.fill(BLACK)

    # Draw the grid
    for row in range(NumRow):
        for column in range(NumCol):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            elif grid[row][column] == 2:
                color = RED
            elif grid[row][column] == 3:
                color = BLUE
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
