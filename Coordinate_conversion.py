import math


def weirdzero(x, y):
    if x != 0:
        fraction = y/x
        # angle = weird_division(num, den)*180/math.pi
        newangle = math.atan(fraction) * 180 / math.pi
        if x < 0:
            newangle += 180
    elif x == 0:
        if y < 0:
            newangle = 270
        elif y > 0:
            newangle = 90
        elif y == 0:
            newangle = 0
    return newangle


def convert_p_to_c(position, radius, angle):
    """converts a given point from polar to cartesian with angle in degrees"""
    x = radius * math.cos((angle * math.pi / 180))
    y = radius * math.sin((angle * math.pi / 180))
    output = [x+position[0], y+position[1]]
    return output


def convert_c_to_p(position):
    """converts a given point from cartesian to polar with angle in degrees"""
    r = math.sqrt((position[0])**2+(position[1]**2))
    angle = weirdzero(position[0], position[1])
    output = [r, angle]
    return output


# print(convert_c_to_p([1, 0]))
