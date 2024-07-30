"""
Filename: main.py
Author: Amitai Ben Shalom
Description: A 3D drawing canvas.

This program allows the user to draw a 2D drawing on the screen and then rotate it in 3D space (see https://en.wikipedia.org/wiki/Solid_of_revolution).
You can also draw while rotating the drawing, thus creating a 3D drawing in real-time.
The program uses rotation matrixes to rotate the drawing in 3D space.
"""

import pygame
import math
from consts import *


def draw_center_lines():
    """
    Draw the center lines on the screen
    """
    global screen
    pygame.draw.line(screen, text_color, (screen_width // 2, 0), (screen_width // 2, screen_height))
    pygame.draw.line(screen, text_color, (0, screen_height // 2), (screen_width, screen_height // 2))


def display_msg(state, dAngle, num_points):
    """
    Display the message on the screen based on the state
    
    Args:
    * state: the state of the program (drawing or showing)
    """
    global screen, msg_font

    if state == State.DRAWING:
        upper_text = msg_font.render(" Draw with the mouse. When finished press 'ENTER' for rotating 360 deg", True, text_color)
        lower_text = msg_font.render(" You can draw while rotating only with RIGHT/LEFT/UP/DOWN keys (not ENTER)", True, text_color)
    else:
        upper_text = msg_font.render(" Use RIGHT/LEFT/UP/DOWN/M/N keys to rotate drawing", True, text_color)
        lower_text = msg_font.render(" Press C to change color and R to reset drawing", True, text_color)
        stats = msg_font.render(f" d-Angle: {dAngle}  |  number of points: {num_points}", True, text_color)
        screen.blit(stats, [0,32])

    screen.blit(upper_text, [0,0])
    screen.blit(lower_text, [0,16])


def valid_point(point, points):
    """
    Check if the point is valid based on the minimum distance from the last point

    Args:
    * point: the point to check
    * points: the list of points to check against
    """
    return len(points) == 0 or math.dist(points[-1], point) > min_distance

    
def size_based_on_y_axis(y):
    """
    Return the size of the point based on the Y axis value)

    Args:
    * y: the input value
    """
    # attempt to create a linear function 
    # return min(max(4, round(0.03 * y + 4)), 8)

    if y <= -44:
        return 3
    elif y < -17:
        return 4
    elif y < 0:
        return 5
    elif y < 17:
        return 5
    elif y < 44:
        return 6
    return 7


def set_dAngle(length):
    """
    Set the dAngle value based on the number of points in the drawing

    Args:
    * length: the number of points in the drawing
    """
    return min(round(0.05 * length + 0.5), 10) # dAngle = 0.05 * length + 0.5 (rounding to nearest integer)


def draw_points(points, color):
    """
    Draw the points on the screen
    
    Args:
    points: list of points to draw
    color: the color to draw the points with (RGB)
    """
    global screen

    for point in points:
        pygame.draw.rect(screen, color, [point[0], point[2], size(point), size(point)])


def rotate3D_Z(vector, angle, center):
    """
    Rotate a 3D vector around the Z axis (implementation of the rotation matrix)

    Args:
    * vector: the vector to rotate
    * angle: the angle to rotate by (in radians)
    * center: the center of the rotation
    """
    pos = [math.cos(angle)*(vector[0]-center[0]) + math.sin(angle)*(vector[1]-center[1]),-math.sin(angle)*(vector[0]-center[0]) + math.cos(angle)*(vector[1]-center[1]), vector[2]]
    pos[0] = pos[0] + center[0]
    pos[1] = pos[1] + center[1]
    return pos


def rotate3D_Y(vector, angle, center):
    """
    Rotate a 3D vector around the Y axis (implementation of the rotation matrix)

    Args:
    * vector: the vector to rotate
    * angle: the angle to rotate by (in radians)
    * center: the center of the rotation
    """
    pos = [math.cos(angle)*(vector[0]-center[0]) + math.sin(angle)*(vector[2]-center[2]),vector[1],-math.sin(angle)*(vector[0]-center[0]) + math.cos(angle)*(vector[2]-center[2])]
    pos[0] = pos[0] + center[0]
    pos[2] = pos[2] + center[2]
    return pos


def rotate3D_X(vector, angle, center):
    """
    Rotate a 3D vector around the X axis (implementation of the rotation matrix)

    Args:
    * vector: the vector to rotate
    * angle: the angle to rotate by (in radians)
    * center: the center of the rotation
    """
    pos = [vector[0],math.cos(angle)*(vector[1]-center[1]) + math.sin(angle)*(vector[2]-center[2]),-math.sin(angle)*(vector[1]-center[1]) + math.cos(angle)*(vector[2]-center[2])]
    pos[1] = pos[1] + center[1]
    pos[2] = pos[2] + center[2]
    return pos


def size(vector):
    """
    Return the size of the point based on the Y axis
    """
    return size_based_on_y_axis(vector[1])


def main():
    """
    The main function of the program (the entry point)
    """
    global drawing_color, dAngle
    points = []  # list of points in the drawing
    center = (screen_width // 2, 0, screen_height // 2)  # the center of the screen (in 3D space, for rotation)
    state = State.DRAWING  # the state of the program (drawing or showing)

    while True:

        for event in pygame.event.get():  # get the events from the user (keyboard, mouse, etc.)
            if event.type == pygame.QUIT:
                return  # if the user presses the 'X' button exit the program
            
            elif event.type == pygame.KEYDOWN:  # if the user presses a key
                if event.key == pygame.K_ESCAPE:
                    return  # if the user presses 'ESC' exit the program

                elif event.key == pygame.K_r:
                    points.clear()  # if the user presses 'R' clear the points
                    state = State.DRAWING  # set the state back to drawing
                
                elif event.key == pygame.K_c:
                    drawing_color = colors[(colors.index(drawing_color) + 1) % len(colors)]  # if the user presses 'C' change the drawing color
                    
                elif state == State.DRAWING and event.key == ENTER_KEY:
                    
                    if len(points) == 0:  # if there are no points, do not continue to the 3D rendering
                        continue
                    
                    length = len(points)  # get the number of points in the drawing (you have to do it here because the points list will be modified)

                    if auto_change_dAngle:
                        dAngle = set_dAngle(length)  # set the dAngle value based on the number of points in the drawing (recommended)
                        # print("length: ", length, "dAngle: ", dAngle)

                    for layer_index in range(360 // dAngle):  # for each layer in the 3D rendering (#layers = 360 degrees divided by dAngle)
                        for point_index in range(length):  # for each point in the drawing rotate it around the Z axis by dAngle
                            rotated_point = rotate3D_Z(points[layer_index * length + point_index], math.radians(-dAngle), center)
                            points.append(rotated_point)  # add the rotated point to the points list
                            pygame.draw.rect(screen, drawing_color, [rotated_point[0], rotated_point[2], size(rotated_point), size(rotated_point)])  # draw the rotated point
                        
                        pygame.display.update()  # update the screen
                        clock.tick(90)  # set the frame rate to maximum 90 frames per second (to prevent the program from crashing and to make the animation smoother)

                    state = State.SHOW  # set the state to showing the 3D drawing
                    # you can now rotate the drawing in 3D space using the arrow keys but you can't draw anymore, only rotate.
                    # this is to prevent the user from generating too many points and crashing the program (each 360 degrees rotation multiplies the number of points by 360/dAngle (which is a lot))
        
        pressed_keys = pygame.key.get_pressed()  # get the keys that are currently pressed by the user

        if pressed_keys[pygame.K_RIGHT]:  # if the user presses the right arrow key rotate the drawing around the Z axis by angle
            for point_index in range(0, len(points)):
                tpoint = rotate3D_Z(points[point_index], math.radians(angle), center)
                points[point_index] = tpoint

        if pressed_keys[pygame.K_LEFT]:  # if the user presses the left arrow key rotate the drawing around the Z axis by -angle
            for point_index in range(0, len(points)):  
                tpoint = rotate3D_Z(points[point_index], math.radians(-angle), center)
                points[point_index] = tpoint

        if pressed_keys[pygame.K_UP]:  # if the user presses the up arrow key rotate the drawing around the X axis by angle
            for point_index in range(0, len(points)):
                tpoint = rotate3D_X(points[point_index], math.radians(angle), center)
                points[point_index] = tpoint

        if pressed_keys[pygame.K_DOWN]:  # if the user presses the down arrow key rotate the drawing around the X axis by -angle
            for point_index in range(0, len(points)):
                tpoint = rotate3D_X(points[point_index], math.radians(-angle), center)
                points[point_index] = tpoint

        if pressed_keys[pygame.K_n]:  # if the user presses the N key rotate the drawing around the Y axis by angle
            for point_index in range(0, len(points)):
                tpoint = rotate3D_Y(points[point_index], math.radians(angle), center)
                points[point_index] = tpoint

        if pressed_keys[pygame.K_m]:  # if the user presses the M key rotate the drawing around the Y axis by -angle
            for point_index in range(0, len(points)):
                tpoint = rotate3D_Y(points[point_index], math.radians(-angle), center)
                points[point_index] = tpoint
                
        if state == State.DRAWING:  # if the state is drawing (you can draw with the mouse)
            if pygame.mouse.get_pressed()[0]:  # if the user presses the left mouse button
                point = (pygame.mouse.get_pos()[0], 0, pygame.mouse.get_pos()[1])  # get the position of the mouse
                if valid_point(point, points):  # if the point is valid (based on the minimum distance from the last point)
                    points.append(point)  # add the point to the points list

        screen.fill(background_color)  # fill the screen with the background color
        draw_center_lines()  # draw the center lines
        display_msg(state, dAngle, len(points))  # display the message based on the state
        draw_points(points, drawing_color)  # draw the points on the screen
        pygame.display.update()  # update the screen
        clock.tick(90)  # set the frame rate to maximum 90 frames per second (to prevent the program from crashing)
            

pygame.init()  # initialize pygame
msg_font = pygame.font.SysFont("bahnschrift", 25)  # set the font for the messages
screen = pygame.display.set_mode((screen_width, screen_height))  # set the screen size
clock = pygame.time.Clock()  # set the clock for the frame rate
pygame.display.set_caption('Rotate Drawing 3D')  # set the title of the window

main()  # call the main function