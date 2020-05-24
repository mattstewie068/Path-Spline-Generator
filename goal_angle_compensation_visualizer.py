import pygame
import Color_List as CL
import My_Functions
import math
import Coordinate_conversion as cc

pygame.init()

SCREENWIDTH = 800
SCREENHEIGHT = 500
WINDOWSIZE = [SCREENWIDTH, SCREENHEIGHT]

zoom_factor = 3

TOP_TO_GOAL = 39
OUTER_GOAL_WIDTH = 36 * zoom_factor
INNER_GOAL_WIDTH = 13 * zoom_factor
GOAL_DEPTH = 29
BALL_SIZE = 7 * zoom_factor

OUTER_GOAL_CENTER = [(SCREENWIDTH / 2), (TOP_TO_GOAL + GOAL_DEPTH)]
INNER_GOAL_CENTER = [(SCREENWIDTH / 2), TOP_TO_GOAL]

# setting up inner goal size
inner_start_pos = int((SCREENWIDTH / 2) - (0.5 * INNER_GOAL_WIDTH))
inner_end_pos = int(inner_start_pos + INNER_GOAL_WIDTH)

outer_start_pos = int((SCREENWIDTH / 2) - ((OUTER_GOAL_WIDTH / 2)))
outer_end_pos = int(outer_start_pos + OUTER_GOAL_WIDTH)


def Draw_Goals():
    """draws frc goal in top middle of field"""
    pygame.draw.line(screen, CL.GREEN, (inner_start_pos, 0), (inner_end_pos, 0), 3)  # draw inner goal
    pygame.draw.line(screen, CL.GREEN, (inner_start_pos, 0), (inner_start_pos, TOP_TO_GOAL), 3)  # draw inner goal
    pygame.draw.line(screen, CL.GREEN, (inner_end_pos, 0), (inner_end_pos, TOP_TO_GOAL), 3)  # draw inner goal

    pygame.draw.line(screen, CL.WHITE, (outer_start_pos, TOP_TO_GOAL),
                     (inner_start_pos, TOP_TO_GOAL), 3)  # draw backboard
    pygame.draw.line(screen, CL.WHITE, (inner_end_pos, TOP_TO_GOAL), (outer_end_pos, TOP_TO_GOAL), 3)  # draw backboard

    pygame.draw.line(
        screen, CL.WHITE, (outer_start_pos, TOP_TO_GOAL),
        (outer_start_pos, TOP_TO_GOAL + (GOAL_DEPTH)),
        3)  # draw depth
    pygame.draw.line(
        screen, CL.WHITE, (outer_end_pos, TOP_TO_GOAL),
        (outer_end_pos, TOP_TO_GOAL + (GOAL_DEPTH)),
        3)  # draw depth

    pygame.draw.line(
        screen, CL.WHITE, (0, TOP_TO_GOAL + GOAL_DEPTH),
        (outer_start_pos, TOP_TO_GOAL + GOAL_DEPTH),
        3)  # draw field wall
    pygame.draw.line(screen, CL.WHITE, (outer_end_pos, TOP_TO_GOAL + GOAL_DEPTH),
                     (SCREENWIDTH, TOP_TO_GOAL + GOAL_DEPTH), 3)  # draw field wall


def Triangle_solver(a, b, angle_c):
    angle_c_rad = cc.degree_to_rad(angle_c)
    c = math.sqrt(b**2 + a**2 - (2 * b * a * math.cos(angle_c_rad)))
    angle_a_rad = math.acos((c**2 + b**2 - a**2) / (2 * c * b))
    angle_a = cc.rad_to_degree(angle_a_rad)
    return angle_a


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

    mousepos = pygame.mouse.get_pos()
    screen.fill(CL.BLACK)
    Draw_Goals()
    pygame.draw.circle(screen, CL.YELLOW, (int(SCREENWIDTH / 2), 15), int((BALL_SIZE) / 2))

    theta = (My_Functions.cursor_angle_to_point(OUTER_GOAL_CENTER) + 180) % 360

    # for debugging only
    innertheta = (My_Functions.angle_between_points(mousepos, INNER_GOAL_CENTER)) % 360
    angle_to_inner_difference = theta - innertheta
    # print(angle_to_inner_difference)

    distance = My_Functions.distance(mousepos, OUTER_GOAL_CENTER)
    # print(distance)

    distance_to_inner = My_Functions.distance(mousepos, INNER_GOAL_CENTER)
    # print(My_Functions.cursor_angle_to_point(OUTER_GOAL_CENTER))

    pygame.draw.line(screen, CL.RED, mousepos, INNER_GOAL_CENTER, 3)

    if theta >= 180 and theta <= 360:
        # draw line from mouse to outer goal center
        pygame.draw.line(screen, CL.RED, mousepos, OUTER_GOAL_CENTER, 3)
        pygame.draw.circle(screen, CL.YELLOW, mousepos, int((BALL_SIZE) / 2))

    if theta >= 192 and theta <= 348:
        pygame.draw.line(screen, CL.GREEN, mousepos, (cc.convert_p_to_c(mousepos, distance, theta)), 3)
        # draw line from mouse at angle and distance

    if theta >= 220 and theta <= 270:
        new_angle = Triangle_solver(GOAL_DEPTH, distance, theta + 90)
        pygame.draw.line(screen, CL.BLUE, mousepos, (cc.convert_p_to_c(
            mousepos, distance_to_inner, new_angle + theta)), 3)

    if theta >= 270 and theta <= 325:
        new_angle = -Triangle_solver(GOAL_DEPTH, distance, theta + 90)
        pygame.draw.line(screen, CL.BLUE, mousepos, (cc.convert_p_to_c(
            mousepos, distance_to_inner, new_angle + theta)), 3)

    pygame.display.flip()

pygame.quit()
