import pygame


class Button():
    def __init__(self, pos, color, showborder=True):
        self.pos = pos
        self.color = color
        self.showborder = showborder
        self.buttonpressed = False


class Rectangle_Button(Button):
    def __init__(self, pos, width, length, color, showborder):
        Button.__init__(self, pos, color, showborder)
        self.width = width
        self.length = length

    def draw(self, screenin):
        """draws a rectangular button with specified parameters"""

    def mouse_in_rectangle(self, func):
        func()
