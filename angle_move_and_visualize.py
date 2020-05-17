import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

WindowHeight = 500
WindowWidth = 1000

radius = 30


def my_function():
    print("Hello from a function")


class Point:
    def __init__(self, pos_in, color_in):
        self.pos = pos_in
        self.color = color_in


myPoint = Point([0, 0], GREEN)
myPoint.color = RED


grid = []
for row in range(WindowHeight):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(WindowHeight):
        grid[row].append(0)  # Append a cell

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [WindowWidth, WindowHeight]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("angle move and visualize")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

pointpos = []

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()

            p = Point(pos, WHITE)
            # Change the x/y screen coordinates to grid coordinates
            if pygame.mouse.get_pressed()[0]:
                p.color = GREEN
            elif pygame.mouse.get_pressed()[1]:
                p.color = RED
            elif pygame.mouse.get_pressed()[2]:
                p.color = BLUE
            pointpos.append(p)
            print(pos, "points: ", pointpos)

    screen.fill(BLACK)
    for current in pointpos:
        pygame.draw.circle(screen, current.color, current.pos, radius)
    # Set the screen background

    background_image = pygame.image.load("clipart arrow.png")
    screen.blit(background_image, [0, 0])


    width = 50
    height = 100
    rectcenter = [300, 200]
    recttransx = (rectcenter[0]-(width/2))
    recttransy = (rectcenter[1]-(height/2))
    pygame.draw.rect(screen, RED, (recttransx, recttransy, width, height))
    pygame.draw.circle(screen, WHITE, rectcenter, 2)
    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
