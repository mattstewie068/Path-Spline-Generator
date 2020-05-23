import math


def weirdzero(x, y):
    if x != 0:
        fraction = y / x
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


def degree_to_rad(rad_angle):
    """input angle in degree, output angle in radian"""
    return (rad_angle * math.pi / 180)


def rad_to_degree(deg_angle):
    """input angle in radian, output angle in degree"""
    return (deg_angle * 180 / math.pi)


def convert_p_to_c(position, radius, angle):
    """converts a given point from polar to cartesian with angle in degrees"""
    x = radius * math.cos(degree_to_rad(angle))
    y = radius * math.sin(degree_to_rad(angle))
    output = [x + position[0], y + position[1]]
    return output


def convert_c_to_p(position):
    """converts a given point from cartesian to polar with angle in degrees"""
    r = math.sqrt((position[0])**2 + (position[1]**2))
    angle = weirdzero(position[0], position[1])
    output = [r, angle]
    return output


# print(convert_c_to_p([1, 0]))
