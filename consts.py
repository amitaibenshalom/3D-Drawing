
from enum import Enum

# ---- screen ----
screen_width = 800
screen_height = 800

# ---- colors ----
# RGB values for colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
blue = (50, 153, 213)
yellow = (255, 255, 102)
green = (0,180,0)
purple = (192,119,210)
colors = [red, blue, yellow, green, purple, black]

background_color = white
drawing_color = red
text_color = black

# ---- 3D rendering ----
dAngle = 10  # the angle resolution (in deg) - this is the angle difference between each iteration when 3D-ing the drawing (smaller -> more details but resource consuming)
angle = 1  # the angle change (in deg) when rotating with arrow keys on each rendered frame (speed of rotation. bigger -> faster)
auto_change_dAngle = True  # change dtheta value automatically based of number of points in drawing (recommended)

min_distance = 5  # the minimum distance between two points in the 3D space (used to avoid division by zero)

# ---- used by program (do not change) ----
class State(Enum):
    DRAWING = 0
    SHOW = 1