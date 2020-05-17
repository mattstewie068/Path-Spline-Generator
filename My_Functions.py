import pygame
import math
import Coordinate_conversion as cc
import Color_List as CL

def equals_with_tolerance(value1, value2, tolerance=1):
    return max(value1, value2) - tolerance <= min(value1, value2)


def pixel_point_to_inch_point(pixels, inches, inputpoint, startx=0, starty=0):
    """takes point in pixel coordinates and converts its position to realworld inch coordinates"""
    conversion = (inches / pixels)
    newx = (inputpoint[0] + startx) * conversion
    newy = (inputpoint[1] + starty) * conversion
    return [newx, newy]


def list_to_inch(lists, windowsize):
    list_in_inch = []
    for number in lists:
        list_in_inch.append(pixel_point_to_inch_point(windowsize[0], 144, number))
    return list_in_inch


def distance(point1, point2):
    """Calculates distance between two specified points [x1,y1] and [x2,y2]"""
    displacementx = point1[0]-point2[0]
    displacementy = point1[1]-point2[1]
    return math.sqrt((displacementx**2)+(displacementy**2))


def cursor_angle_to_point(pointposition):
    mousepos = pygame.mouse.get_pos()
    relmouseposx = mousepos[0] - pointposition[0]
    relmouseposy = mousepos[1] - pointposition[1]
    relmousepos = [relmouseposx, relmouseposy]
    return cc.convert_c_to_p(relmousepos)[1]


def addline(screen, point1, point2):
    """
    avered = (circle1.color[0] + circle2.color[0])/2
    avegreen = (circle1.color[1] + circle2.color[1])/2
    aveblue = (circle1.color[2] + circle2.color[2])/2
    linecolor = [avered,avegreen,aveblue]
    pygame.draw.line(screen, linecolor, circle1.pos, circle2.pos, 2)
    """
    pygame.draw.line(screen, CL.RED, point1.pointpos, point2.pointpos, 2)


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


def duplicatept(lists):
    for points in range(len(lists)-1):
        if lists[points] == lists[points+1]:
            return True





# def add_angle_to_pt(pointlist, anglelist):
#     list_with_angle = []
#     pass


def next_robot_location():
    return next()
