
from enum import Enum

dTheta = 10  # the angle resolution - this is the angle difference between each iteration when 3D-ing the drawing (smaller -> more details)

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
blue = (50, 153, 213)
yellow = (255, 255, 102)
green = (0,180,0)
purple = (192,119,210)

screen_width = 800
screen_height = 800

background_color = white
drawing_color = red

class State(Enum):
    DRAWING = 0
    SHOW = 1


colors = [red, blue, yellow, green, purple, black]


