import pygame
import Color_List as CL
import My_Functions

pygame.init()

SCREENWIDTH = 800
SCREENHEIGHT = 500
WINDOWSIZE = [SCREENWIDTH, SCREENHEIGHT]

zoom_factor = 3

TOP_TO_GOAL = 30
OUTER_GOAL_WIDTH = 36
INNER_GOAL_WIDTH = 13
GOAL_DEPTH = 29
BALL_SIZE = 7

OUTER_GOAL_CENTER = [int(SCREENWIDTH / 2), (TOP_TO_GOAL + GOAL_DEPTH)]

# setting up inner goal size
inner_start_pos = int((SCREENWIDTH / 2) - (0.5 * INNER_GOAL_WIDTH * zoom_factor))
inner_end_pos = int(inner_start_pos + INNER_GOAL_WIDTH * zoom_factor)

outer_start_pos = int((SCREENWIDTH / 2) - ((OUTER_GOAL_WIDTH / 2) * zoom_factor))
outer_end_pos = int(outer_start_pos + OUTER_GOAL_WIDTH * zoom_factor)


def Draw_Goals():
    """draws frc goal in top middle of field"""
    pygame.draw.line(screen, CL.GREEN, (inner_start_pos, 0), (inner_end_pos, 0), 3)  # draw inner goal
    pygame.draw.line(screen, CL.GREEN, (inner_start_pos, 0), (inner_start_pos, TOP_TO_GOAL), 3)  # draw inner goal
    pygame.draw.line(screen, CL.GREEN, (inner_end_pos, 0), (inner_end_pos, TOP_TO_GOAL), 3)  # draw inner goal

    pygame.draw.line(screen, CL.RED, (outer_start_pos, TOP_TO_GOAL),
                     (inner_start_pos, TOP_TO_GOAL), 3)  # draw backboard
    pygame.draw.line(screen, CL.RED, (inner_end_pos, TOP_TO_GOAL), (outer_end_pos, TOP_TO_GOAL), 3)  # draw backboard

    pygame.draw.line(
        screen, CL.RED, (outer_start_pos, TOP_TO_GOAL),
        (outer_start_pos, TOP_TO_GOAL + GOAL_DEPTH),
        3)  # draw depth
    pygame.draw.line(
        screen, CL.RED, (outer_end_pos, TOP_TO_GOAL),
        (outer_end_pos, TOP_TO_GOAL + GOAL_DEPTH),
        3)  # draw depth

    pygame.draw.line(
        screen, CL.WHITE, (0, TOP_TO_GOAL + GOAL_DEPTH),
        (outer_start_pos, TOP_TO_GOAL + GOAL_DEPTH),
        3)  # draw field wall
    pygame.draw.line(screen, CL.WHITE, (outer_end_pos, TOP_TO_GOAL + GOAL_DEPTH),
                     (SCREENWIDTH, TOP_TO_GOAL + GOAL_DEPTH), 3)  # draw field wall

def Inner_Angle():
    pass

clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOWSIZE)

pygame.display.set_caption("Goal Angle Compensation Visualizer")

RUN = True

while RUN:  # run until quit
    for event in pygame.event.get():  # loop through all events sinse last loop
        if event.type == pygame.QUIT:
            RUN = False
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            RUN = False

    pygame.draw.circle(screen, CL.YELLOW, (int(SCREENWIDTH / 2), 15), int((BALL_SIZE * zoom_factor) / 2))

    angle = My_Functions.cursor_angle_to_point(OUTER_GOAL_CENTER)
    mousepos = pygame.mouse.get_pos()
    distance = My_Functions.distance(mousepos, OUTER_GOAL_CENTER)

    screen.fill(CL.BLACK)
    Draw_Goals()
    pygame.draw.circle(screen, CL.YELLOW, mousepos, int((BALL_SIZE * zoom_factor) / 2))
    pygame.draw.line(screen, CL.PURPLE, mousepos, OUTER_GOAL_CENTER, 3)  # draw line from mouse to outer goal center

    pygame.display.flip()

pygame.quit()
