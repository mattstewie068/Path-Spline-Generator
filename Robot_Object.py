import My_Functions
import Color_List as CL
import pygame

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
        a = My_Functions.equals_with_tolerance(self.pos[0], destination[0])
        b = My_Functions.equals_with_tolerance(self.pos[1], destination[1])
        return a == b

    def draw(self, screenin):
        if self.drawyn:
            recttransx = (self.pos[0]-(self.width/2))
            recttransy = (self.pos[1]-(self.length/2))
            pygame.draw.rect(screenin, CL.BLUE, (recttransx, recttransy, self.width, self.length))
            pygame.draw.circle(screenin, CL.WHITE, My_Functions.list_to_ints(self.pos), 2)
