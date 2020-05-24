import pygame
import Color_List as CL
import My_Functions
import math
import Coordinate_conversion as cc

pygame.init()

# setup screen dimentions
SCREENWIDTH = 800
SCREENHEIGHT = 500
WINDOWSIZE = [SCREENWIDTH, SCREENHEIGHT]

zoom_factor = 3  # scaling to make inch counts in pixels more visable

TOP_TO_GOAL = 39  # distance from screen top to back of inner goal
OUTER_GOAL_WIDTH = 36 * zoom_factor
INNER_GOAL_WIDTH = 13 * zoom_factor
GOAL_DEPTH = 29 * zoom_factor
BALL_SIZE = 7 * zoom_factor  # diameter of ball

# calculating centerpoint for inner and outer goal
OUTER_GOAL_CENTER = [(SCREENWIDTH / 2), (TOP_TO_GOAL + GOAL_DEPTH)]
INNER_GOAL_CENTER = [(SCREENWIDTH / 2), TOP_TO_GOAL]

# setting up inner goal size
inner_start_pos = int((SCREENWIDTH / 2) - (0.5 * INNER_GOAL_WIDTH))
inner_end_pos = int(inner_start_pos + INNER_GOAL_WIDTH)

# setting up outer goal size
outer_start_pos = int((SCREENWIDTH / 2) - ((OUTER_GOAL_WIDTH / 2)))
outer_end_pos = int(outer_start_pos + OUTER_GOAL_WIDTH)


def Draw_Goals():
    """draws frc goal in top middle of field"""

    # draw inner goal
    pygame.draw.line(screen, CL.GREEN, (inner_start_pos, 0), (inner_end_pos, 0), 3)
    pygame.draw.line(screen, CL.GREEN, (inner_start_pos, 0), (inner_start_pos, TOP_TO_GOAL), 3)
    pygame.draw.line(screen, CL.GREEN, (inner_end_pos, 0), (inner_end_pos, TOP_TO_GOAL), 3)

    # draw backboard
    pygame.draw.line(screen, CL.WHITE, (outer_start_pos, TOP_TO_GOAL), (inner_start_pos, TOP_TO_GOAL), 3)
    pygame.draw.line(screen, CL.WHITE, (inner_end_pos, TOP_TO_GOAL), (outer_end_pos, TOP_TO_GOAL), 3)

    # draw depth
    pygame.draw.line(
        screen, CL.WHITE, (outer_start_pos, TOP_TO_GOAL), (outer_start_pos, TOP_TO_GOAL + (GOAL_DEPTH)), 3)
    pygame.draw.line(
        screen, CL.WHITE, (outer_end_pos, TOP_TO_GOAL), (outer_end_pos, TOP_TO_GOAL + (GOAL_DEPTH)), 3)

    # draw field wall
    pygame.draw.line(
        screen, CL.WHITE, (0, TOP_TO_GOAL + GOAL_DEPTH), (outer_start_pos, TOP_TO_GOAL + GOAL_DEPTH), 3)
    pygame.draw.line(
        screen, CL.WHITE, (outer_end_pos, TOP_TO_GOAL + GOAL_DEPTH), (SCREENWIDTH, TOP_TO_GOAL + GOAL_DEPTH), 3)

    # draw ball in inner goal
    pygame.draw.circle(screen, CL.YELLOW, (int(SCREENWIDTH / 2), 15), int((BALL_SIZE) / 2))


def Triangle_solver_side_c(a, b, angle_C):
    angle_C_rad = cc.degree_to_rad(angle_C)
    c = math.sqrt(b**2 + a**2 - (2 * b * a * math.cos(angle_C_rad)))
    return c


def Triangle_solver_angle_A(a, b, angle_C):
    c = Triangle_solver_side_c(a, b, angle_C)
    angle_A_rad = math.acos((c**2 + b**2 - a**2) / (2 * c * b))
    angle_A = cc.rad_to_degree(angle_A_rad)
    return angle_A


clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOWSIZE)

pygame.display.set_caption("Goal Angle Compensation Visualizer")

RUN = True

while RUN:  # run until quit
    for event in pygame.event.get():  # loop through all events sinse last loop

        # conditions to quit running game
        if event.type == pygame.QUIT:  # press the close button
            RUN = False
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            RUN = False

    mousepos = pygame.mouse.get_pos()
    screen.fill(CL.BLACK)
    Draw_Goals()

    # given inputs
    beta = (My_Functions.cursor_angle_to_point(OUTER_GOAL_CENTER)) % 360  # angle of cursor to outer goal
    distance_to_outer = My_Functions.distance(mousepos, OUTER_GOAL_CENTER)  # distance from cursor to outer goal

    Point_B = [0, 0]
    alpha = 0

    # depending on mouse angle beta calculate triangle
    if beta >= 0 and beta < 90:  # calculate point to draw to when mouse is on right side of screen
        theta = beta
        angle_c = theta + 90
        angle_a = Triangle_solver_angle_A(GOAL_DEPTH, distance_to_outer, angle_c)
        side_c = Triangle_solver_side_c(GOAL_DEPTH, distance_to_outer, angle_c)

        alpha = angle_a + beta
        x = side_c * math.cos(cc.degree_to_rad(alpha))
        y = side_c * math.sin(cc.degree_to_rad(alpha))

        Point_B = [mousepos[0] - x, mousepos[1] - y]

    elif beta == 90:  # calculate point to draw to when mouse is directly infront of goal
        side_c = GOAL_DEPTH + distance_to_outer
        Point_B = [mousepos[0], mousepos[1] - side_c]

    elif beta > 90 and beta <= 180:  # calculate point to draw to when mouse is on left side of screen
        theta = 180 - beta
        angle_c = theta + 90
        angle_a = Triangle_solver_angle_A(GOAL_DEPTH, distance_to_outer, angle_c)
        side_c = Triangle_solver_side_c(GOAL_DEPTH, distance_to_outer, angle_c)

        alpha = angle_a + theta
        x = side_c * math.cos(cc.degree_to_rad(alpha))
        y = side_c * math.sin(cc.degree_to_rad(alpha))

        Point_B = [mousepos[0] + x, mousepos[1] - y]

    OUTER_GOAL_CENTER = My_Functions.list_to_ints(OUTER_GOAL_CENTER)
    Point_B = My_Functions.list_to_ints(Point_B)

    # draw lines
    if beta >= 0 and beta <= 180:  # if cursor is below field wall draw stuff
        pygame.draw.circle(screen, CL.YELLOW, mousepos, int((BALL_SIZE) / 2))
        # print(alpha)
        # draw red no shot available lines
        if alpha > 0 and alpha <= 90:  # draw red no shot line to inner goal
            #print("0-30", alpha)
            pygame.draw.line(screen, CL.RED, mousepos, Point_B, 3)
        if beta > 0 and beta <= 14:  # draw red no shot line to outer goal
            pygame.draw.line(screen, CL.RED, mousepos, OUTER_GOAL_CENTER, 3)

        elif alpha > 30 and alpha < 90:  # draw shots for right side of screen
            # print(alpha)
            if alpha > 30 and alpha <= 65:  # draw green outer goal line and red line for inner goal
                pygame.draw.line(screen, CL.GREEN, mousepos, OUTER_GOAL_CENTER, 3)
                pygame.draw.line(screen, CL.RED, mousepos, Point_B, 3)
            elif alpha > 65 and alpha <= 90:  # draw blue inner goal line and green outer goal line
                pygame.draw.line(screen, CL.GREEN, mousepos, OUTER_GOAL_CENTER, 3)
                pygame.draw.line(screen, CL.BLUE, mousepos, Point_B, 3)
        if beta > 166 and beta <= 180:  # draw red no shot line to outer goal
            pygame.draw.line(screen, CL.RED, mousepos, OUTER_GOAL_CENTER, 3)

        elif alpha == 0:  # draw blue inner goal line only
            #print("0 alpha")
            pygame.draw.line(screen, CL.BLUE, mousepos, Point_B, 3)

    elif beta > 180 and beta < 360:
        print("Get Back on the Field!")

    pygame.display.flip()

pygame.quit()
