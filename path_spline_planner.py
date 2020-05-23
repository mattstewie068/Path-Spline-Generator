
import sys
sys.path.append('C:\\Users\\matts\\Desktop\\Python Practice\\Arduino Stuff')
import Robot_Object
import My_Functions
import Point_Objects
import Color_List as CL
import splines
import pygame
import csv
import pickle
# pylint: disable=import-error
import segment_display as sd
# pylint: enable=import-error


def addpoint(mousepos, pointtype="general", drawyn=True):
    points_count = len(list_of_points)
    list_of_points.insert((points_count - 1), Point_Objects.Point(mousepos, pointtype, drawyn))


def update_fps():
    """returns current FPS value"""
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 2, CL.CYAN)
    return fps_text


def steps(start, end, pointcount):
    """Calculates evenly spaced points between two values"""
    if n < 2:
        raise Exception("behaviour not defined for n<2")
    step = (end - start) / float(pointcount - 1)
    return [(start + x * step) for x in range(pointcount)]


pygame.init()

list_of_points = [Point_Objects.Point([400, 50], "start", True), Point_Objects.Point([400, 200], "end", True)]


# SCREENWIDTH = 942
# SCREENHEIGHT = 378
# WINDOWSIZE = [SCREENWIDTH, SCREENHEIGHT]


background_image = pygame.image.load("FTC Field.png")
WINDOWSIZE = background_image.get_size()

# print(inch_to_pixel(WINDOWSIZE[0], 144, [1,1]))

font = pygame.font.SysFont("Arial", 18)

clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOWSIZE)

pygame.display.set_caption("Point Map and Path Creator")


# print(background_image.get_size())
RUN = True
c = []
c_inch = []
inputlist = []
ROBOT_CURRENT_POSITION = 0
my_robot = Robot_Object.Robot([0, 0])

while RUN:  # run until quit
    GENERATESPLINE = False
    for event in pygame.event.get():  # loop through all events sinse last loop
        if event.type == pygame.QUIT:
            RUN = False
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            RUN = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:
                addpoint(list(pygame.mouse.get_pos()), "direction")
                GENERATESPLINE = True

            if pygame.mouse.get_pressed()[1]:
                for point in reversed(list_of_points):
                    if point.mouseinpoint():
                        list_of_points.pop(list_of_points.index(point))
                        GENERATESPLINE = True

            if pygame.mouse.get_pressed()[0]:
                for point in reversed(list_of_points):
                    if point.mouseinpoint():
                        point.moving = True
                        GENERATESPLINE = True
                        break
                    elif point.mouseinarrow():
                        point.rotating = True
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            for point in list_of_points:
                point.moving = False
                point.rotating = False

        if event.type == pygame.MOUSEMOTION:
            for point in list_of_points:
                if point.moving:
                    point.move(event.rel)
                    GENERATESPLINE = True

        for point in reversed(list_of_points):
            point.rotate()

        if event.type == pygame.KEYDOWN:
            pygame.key.set_repeat()

            if pygame.key.get_pressed()[pygame.K_b]:
                addpoint(list(pygame.mouse.get_pos()))
                GENERATESPLINE = True

            if pygame.key.get_pressed()[pygame.K_s]:
                with open('storage', 'wb') as f:
                    pickle.dump(list_of_points, f)
                sd.display_saved()
            if pygame.key.get_pressed()[pygame.K_l]:
                with open('storage', 'rb') as f:
                    list_of_points = pickle.load(f)
                    GENERATESPLINE = True
                sd.display_loaded()
            if pygame.key.get_pressed()[pygame.K_e]:
                with open("exported data.csv", "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerows(c_inch)
                print("Data Exported!")

    screen.fill(CL.BLACK)
    screen.blit(background_image, [0, 0])

    for point in list_of_points:
        point.draw(screen)

    for n in range(len(list_of_points) - 1):
        My_Functions.addline(screen, list_of_points[n], list_of_points[n + 1])

    if My_Functions.duplicatept(list_of_points):
        GENERATESPLINE = False

    if len(list_of_points) >= 4:
        if GENERATESPLINE:
            Chain = []  # Calculate the Catmull-Rom splines through the points

            for point in list_of_points:
                Chain.append((point.pointpos[0], point.pointpos[1]))

            PTS_PER_SPLINE = 100

            # "c" is all points created by spline code in pixel coordinates
            c = splines.CatmullRomChain(Chain, PTS_PER_SPLINE)

            ROBOT_CURRENT_POSITION = 0
            my_robot.pos = c[ROBOT_CURRENT_POSITION]

        if not GENERATESPLINE and sd.switch_1_state():
            my_robot.pos = c[ROBOT_CURRENT_POSITION]
            my_robot.draw(screen)

            ROBOT_CURRENT_POSITION += 1
            if ROBOT_CURRENT_POSITION == len(c):
                ROBOT_CURRENT_POSITION = 0

        for npts in range(len(c) - 1):
            pygame.draw.line(screen, CL.WHITE, My_Functions.list_to_ints(
                c[npts]), My_Functions.list_to_ints(c[npts + 1]), 3)

    # convert c from pixels to inches
    c_inch = My_Functions.list_to_inch(c, WINDOWSIZE[0])

    clock.tick(200 * sd.pot_1_state())
    screen.blit(update_fps(), (10, 5))

    pygame.display.flip()

pygame.quit()

# end of File
