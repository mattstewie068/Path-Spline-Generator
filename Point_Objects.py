import pygame
import Color_List as CL
from numpy.random import randint
import Coordinate_conversion as cc
import My_Functions

class Arrow():
    def __init__(self, pos, arrowangle, radius=50):
        self.arrowpos = pos
        self.arrowangle = arrowangle
        self.radius = radius
        self.circle = Circle(self.calc_circle_center(), 10, CL.CYAN, 1, True)
        self.rotating = False

    def calc_circle_center(self):
        return [round(cc.convert_p_to_c(self.arrowpos, self.radius, self.arrowangle)[0]), round(cc.convert_p_to_c(self.arrowpos, self.radius, self.arrowangle)[1])]

    def draw(self, screenin):
        pygame.draw.line(screenin, CL.CYAN, self.arrowpos, self.calc_circle_center(), 3)
        self.circle.draw(screenin)

    def move(self, movedistance):
        """moves circle specified distance"""
        self.arrowpos[0] = movedistance[0]
        self.arrowpos[1] = movedistance[1]
        self.circle.move(self.calc_circle_center())

    def rotate(self):
        self.arrowangle = My_Functions.cursor_angle_to_point(self.arrowpos)
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
        distancebetweenpoints = My_Functions.distance(mousepos, self.circlepos)
        inside = distancebetweenpoints <= self.rad
        return inside

    def move(self, movedistance):
        """moves circle specified distance"""
        self.circlepos[0] = movedistance[0]
        self.circlepos[1] = movedistance[1]

    def draw(self, screenin):
        """draws circle with specified parameters"""
        if self.showborder:
            pygame.draw.circle(screenin, self.color, self.circlepos, self.rad, self.border)
        else:
            pygame.draw.circle(screenin, self.color, self.circlepos, self.rad)


class Point():
    def __init__(self, pos, point_type, drawyn=True):
        self.pointpos = pos
        self.moving = False
        self.rotating = False
        self.drawyn = drawyn

        if point_type == "start":
            self.circle = Circle(self.pointpos, 10, CL.GREEN, 10, False)
            self.arrow = Arrow(pos, 180)
            self.arrowyesorno = True
            self.circleyesorno = True

        elif point_type == "end":
            self.circle = Circle(self.pointpos, 10, CL.RED, 10, False)
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

    def draw(self, screenin):
        if self.drawyn:
            if self.arrowyesorno:
                self.arrow.draw(screenin)
            if self.circleyesorno:
                self.circle.draw(screenin)

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
