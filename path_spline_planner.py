import Coordinate_conversion as cc
import splines
from numpy.random import randint
import pygame
import math
import pickle
import csv

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PINK = (255, 105, 180)


class Arrow():
    def __init__(self, pos, arrowangle, radius=50):
        self.arrowpos = pos
        self.arrowangle = arrowangle
        self.radius = radius
        self.circle = Circle(self.calc_circle_center(), 10, CYAN, 1, True)
        self.rotating = False

    def calc_circle_center(self):
        return [round(cc.convert_p_to_c(self.arrowpos, self.radius, self.arrowangle)[0]), round(cc.convert_p_to_c(self.arrowpos, self.radius, self.arrowangle)[1])]

    def draw(self):
        pygame.draw.line(screen, CYAN, self.arrowpos, self.calc_circle_center(), 3)
        self.circle.draw()

    def move(self, movedistance):
        """moves circle specified distance"""
        self.arrowpos[0] = movedistance[0]
        self.arrowpos[1] = movedistance[1]
        self.circle.move(self.calc_circle_center())

    def rotate(self):
        self.arrowangle = cursor_angle_to_point(self.arrowpos)
        self.circle.move(self.calc_circle_center())

    def mouseinarrow(self):
        """returns boleen telling whether mouse is in given circle or not"""
        return self.circle.mouseincircle()


class Circle():
    def __init__(self, pos, rad, color, border, showborder):
        """initializes the circle object"""
        self.circlepos = pos
        self.rad = rad
        self.color = color
        self.moving = False
        self.border = border
        self.showborder = showborder

    def __str__(self):
        return "the circles position is " + str(self.circlepos)

    def mouseincircle(self):
        """returns boleen telling whether mouse is in given circle or not"""
        mousepos = pygame.mouse.get_pos()
        distancebetweenpoints = distance(mousepos, self.circlepos)
        inside = distancebetweenpoints <= self.rad
        return inside

    def move(self, movedistance):
        """moves circle specified distance"""
        self.circlepos[0] = movedistance[0]
        self.circlepos[1] = movedistance[1]

    def draw(self):
        """draws circle with specified parameters"""
        if self.showborder:
            pygame.draw.circle(screen, self.color, self.circlepos, self.rad, self.border)
        else:
            pygame.draw.circle(screen, self.color, self.circlepos, self.rad)


class Point():
    def __init__(self, pos, point_type, drawyn=True):
        self.pointpos = pos
        self.moving = False
        self.rotating = False
        self.drawyn = drawyn

        if point_type == "start":
            self.circle = Circle(self.pointpos, 10, GREEN, 10, False)
            self.arrow = Arrow(pos, 180)
            self.arrowyesorno = True
            self.circleyesorno = True

        elif point_type == "end":
            self.circle = Circle(self.pointpos, 10, RED, 10, False)
            self.arrow = Arrow(pos, 90)
            self.arrowyesorno = True
            self.circleyesorno = True

        elif point_type == "general":
            rand_color = (randint(0, 255), randint(0, 255), randint(0, 255))
            self.circle = Circle(self.pointpos, 10, rand_color, 2, True)
            self.arrowyesorno = False
            self.circleyesorno = True

        elif point_type == "direction":
            rand_color = (randint(0, 255), randint(0, 255), randint(0, 255))
            self.circle = Circle(self.pointpos, 10, rand_color, 2, True)
            self.arrow = Arrow(pos, 90)
            self.arrowyesorno = True
            self.circleyesorno = True

        else:
            print("point_type error")

    def move(self, movedistance):
        """moves point specified distance"""
        self.pointpos[0] += movedistance[0]
        self.pointpos[1] += movedistance[1]
        if self.circleyesorno:
            self.circle.move(self.pointpos)
        if self.arrowyesorno:
            self.arrow.move(self.pointpos)

    def draw(self):
        if self.drawyn:
            if self.arrowyesorno:
                self.arrow.draw()
            if self.circleyesorno:
                self.circle.draw()

    def mouseinpoint(self):
        """returns boleen telling whether mouse is in given circle or not"""
        return self.circle.mouseincircle()

    def mouseinarrow(self):
        """returns boleen telling whether mouse is in given arrow or not"""
        if self.arrowyesorno:
            return self.arrow.mouseinarrow()

    def rotate(self):
        if self.arrowyesorno and self.rotating:
            self.arrow.rotate()

    # width = 50
    # height = 100
    # rectangle = [650, 300]
    # center = rectcenter(rectangle, width, height)
    # pygame.draw.rect(screen, RED, (center[0], center[1], width, height))
    # pygame.draw.circle(screen, WHITE, rectangle, 2)


class Robot():
    def __init__(self, pos, drawyn=True, length=50, width=40, speed=.5):
        self.drawyn = drawyn
        self.pos = pos
        self.length = length
        self.width = width
        self.speed = speed

    def move(self, destination):
        relx = destination[0] - self.pos[0]
        rely = destination[1] - self.pos[1]
        xnormalized = relx / max(abs(relx), abs(rely))
        ynormalized = rely / max(abs(relx), abs(rely))
        moveamount = [xnormalized * self.speed, ynormalized * self.speed]
        self.pos[0] += moveamount[0]
        self.pos[1] += moveamount[1]
        a = equals_with_tolerance(self.pos[0], destination[0])
        b = equals_with_tolerance(self.pos[1], destination[1])
        return a == b

    def draw(self):
        if self.drawyn:
            recttransx = (self.pos[0]-(self.width/2))
            recttransy = (self.pos[1]-(self.length/2))
            pygame.draw.rect(screen, BLUE, (recttransx, recttransy, self.width, self.length))
            pygame.draw.circle(screen, WHITE, list_to_ints(self.pos), 2)


def equals_with_tolerance(value1, value2, tolerance=1):
    return max(value1, value2) - tolerance <= min(value1, value2)


def pixel_point_to_inch_point(pixels, inches, inputpoint, startx=0, starty=0):
    """takes point in pixel coordinates and converts its position to realworld inch coordinates"""
    conversion = (inches / pixels)
    newx = (inputpoint[0] + startx) * conversion
    newy = (inputpoint[1] + starty) * conversion
    return [newx, newy]


def list_to_inch(lists):
    list_in_inch = []
    for number in lists:
        list_in_inch.append(pixel_point_to_inch_point(WINDOWSIZE[0], 144, number))
    return list_in_inch


def distance(point1, point2):
    """Calculates distance between two specified points [x1,y1] and [x2,y2]"""
    displacementx = point1[0]-point2[0]
    displacementy = point1[1]-point2[1]
    return math.sqrt((displacementx**2)+(displacementy**2))


def addpoint(mousepos, pointtype="general", drawyn=True):
    points_count = len(list_of_points)
    list_of_points.insert((points_count-1), Point(mousepos, pointtype, drawyn))


def cursor_angle_to_point(pointposition):
    mousepos = pygame.mouse.get_pos()
    relmouseposx = mousepos[0] - pointposition[0]
    relmouseposy = mousepos[1] - pointposition[1]
    relmousepos = [relmouseposx, relmouseposy]
    return cc.convert_c_to_p(relmousepos)[1]


def addline(point1, point2):
    """
    avered = (circle1.color[0] + circle2.color[0])/2
    avegreen = (circle1.color[1] + circle2.color[1])/2
    aveblue = (circle1.color[2] + circle2.color[2])/2
    linecolor = [avered,avegreen,aveblue]
    pygame.draw.line(screen, linecolor, circle1.pos, circle2.pos, 2)
    """
    pygame.draw.line(screen, RED, point1.pointpos, point2.pointpos, 2)


def rectcenter(desiredcenter, rectwidth, rectheight):
    """Calculates where the corner of a rectangle should be given the desired center pt and size"""
    recttransx = int(desiredcenter[0]-(rectwidth/2))
    recttransy = int(desiredcenter[1]-(rectheight/2))
    return recttransx, recttransy


def roundlist(lists, decimals):
    roundedlist = []
    for element in lists:
        roundedlist.append(round(element, decimals))
    return roundedlist


def round_list_of_lists(list_of_lists, decimals):
    """returns a list of lists with all values rounded to a cpecifie decimal place"""
    list_of_lists_rounded = []
    for i in list_of_lists:
        list_of_lists_rounded.append(roundlist(i, decimals))
    return list_of_lists_rounded


def list_to_ints(lists):
    listofints = []
    for element in lists:
        if math.isnan(element):
            listofints.append(0)
        else:
            listofints.append(int(element))
    return listofints


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 2, CYAN)
    return fps_text


def duplicatept(lists):
    for points in range(len(lists)-1):
        if lists[points] == lists[points+1]:
            return True


def steps(start, end, pointcount):
    if n < 2:
        raise Exception("behaviour not defined for n<2")
    step = (end-start)/float(pointcount-1)
    return [(start+x*step) for x in range(pointcount)]


# def add_angle_to_pt(pointlist, anglelist):
#     list_with_angle = []
#     pass


def next_robot_location():
    return next()


pygame.init()

list_of_points = [Point([400, 50], "start", True), Point([400, 200], "end", True)]


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
robot_current_position = 0
my_robot = Robot([0, 0])

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
                print("Points Saved!")
            if pygame.key.get_pressed()[pygame.K_l]:
                with open('storage', 'rb') as f:
                    list_of_points = pickle.load(f)
                    GENERATESPLINE = True
                print("Points Loaded!")
            if pygame.key.get_pressed()[pygame.K_e]:
                with open("exported data.csv", "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerows(c_inch)
                print("Data Exported!")

    screen.fill(BLACK)
    screen.blit(background_image, [0, 0])

    for point in list_of_points:
        point.draw()

    for n in range(len(list_of_points)-1):
        addline(list_of_points[n], list_of_points[n+1])

    if duplicatept(list_of_points):
        GENERATESPLINE = False

    if len(list_of_points) >= 4:
        if GENERATESPLINE:
            Chain = []  # Calculate the Catmull-Rom splines through the points

            for point in list_of_points:
                Chain.append((point.pointpos[0], point.pointpos[1]))

            PTS_PER_SPLINE = 100

            # "c" is all points created by spline code in pixel coordinates
            c = splines.CatmullRomChain(Chain, PTS_PER_SPLINE)

            robot_current_position = 0
            my_robot.pos = c[robot_current_position]

        if not GENERATESPLINE:
            my_robot.pos = c[robot_current_position]
            my_robot.draw()

            robot_current_position += 1
            if robot_current_position == len(c):
                robot_current_position = 0

        for npts in range(len(c)-1):
            pygame.draw.line(screen, WHITE, list_to_ints(c[npts]), list_to_ints(c[npts+1]), 3)

    # convert c from pixels to inches
    c_inch = list_to_inch(c)

    clock.tick()
    screen.blit(update_fps(), (10, 5))

    pygame.display.flip()

pygame.quit()
