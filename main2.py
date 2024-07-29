"""
Filename: main.py
Author: Amitai Ben Shalom
Description: A 3D drawing program using pygame and math. TODO: write more
"""

import pygame
import math
from consts import *


def draw_center_lines():
    global screen
    pygame.draw.line(screen, black, (screen_width // 2, 0), (screen_width // 2, screen_height))
    pygame.draw.line(screen, black, (0, screen_height // 2), (screen_width, screen_height // 2))


def display_start_msg():
    global screen, msg_font
    text = msg_font.render("Draw with the mouse. When finished press '3' for 3D or '2' for 2D", True, black)
    screen.blit(text, [0,0])
    
def realSigmoid(x):
    if x<=-44:
        return 2
    elif x < -17:
        return 3
    elif x < 0:
        return 4
    elif x < 17:
        return 5
    elif x < 44:
        return 6
    return 7

def draw_points(points, color):
    global screen
    for point in points:
        pygame.draw.rect(screen, color, [point[0], point[2], size(point), size(point)])


def rotate3D_Z(vector, angle, center):
    pos = [math.cos(angle)*(vector[0]-center[0]) + math.sin(angle)*(vector[1]-center[1]),-math.sin(angle)*(vector[0]-center[0]) + math.cos(angle)*(vector[1]-center[1]), vector[2]]
    pos[0] = pos[0] + center[0]
    pos[1] = pos[1] + center[1]
    return pos

def rotate3D_Y(vector, angle, center):
    pos = [math.cos(angle)*(vector[0]-center[0]) + math.sin(angle)*(vector[2]-center[2]),vector[1],-math.sin(angle)*(vector[0]-center[0]) + math.cos(angle)*(vector[2]-center[2])]
    pos[0] = pos[0] + center[0]
    pos[2] = pos[2] + center[2]
    return pos

def rotate3D_X(vector, angle, center):
    pos = [vector[0],math.cos(angle)*(vector[1]-center[1]) + math.sin(angle)*(vector[2]-center[2]),-math.sin(angle)*(vector[1]-center[1]) + math.cos(angle)*(vector[2]-center[2])]
    pos[1] = pos[1] + center[1]
    pos[2] = pos[2] + center[2]
    return pos


def size(vector):
    return realSigmoid(vector[1])


def main():
    global drawing_color
    points = []
    theta = 2
    center = (screen_width // 2, 0, screen_height // 2)
    state = State.DRAWING

    while True:
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return
            
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return
                
                elif event.key == pygame.K_r:
                    points.clear()
                    state = State.DRAWING
                
                elif event.key == pygame.K_c:
                    drawing_color = colors[(colors.index(drawing_color) + 1) % len(colors)]
                    
                elif state == State.DRAWING and event.key == pygame.K_3:
                    
                    if len(points) == 0:
                        continue
                    
                    length = len(points)
                    for layer_index in range(360 // dTheta):
                        for point_index in range(length):
                            rotated_point = rotate3D_Z(points[layer_index * length + point_index], math.radians(-dTheta), center)
                            points.append(rotated_point)
                            pygame.draw.rect(screen, drawing_color, [rotated_point[0], rotated_point[2], size(rotated_point), size(rotated_point)])
                        pygame.display.update()
                        clock.tick(90)
                    state = State.SHOW
        
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT]:
            for point_index in range(0, len(points)):
                tpoint = rotate3D_Z(points[point_index], math.radians(-theta), center)
                points[point_index] = tpoint

        if pressed_keys[pygame.K_RIGHT]:
            for point_index in range(0, len(points)):
                tpoint = rotate3D_Z(points[point_index], math.radians(theta), center)
                points[point_index] = tpoint

        if pressed_keys[pygame.K_UP]:
            for point_index in range(0, len(points)):
                tpoint = rotate3D_X(points[point_index], math.radians(theta), center)
                points[point_index] = tpoint

        if pressed_keys[pygame.K_DOWN]:
            for point_index in range(0, len(points)):
                tpoint = rotate3D_X(points[point_index], math.radians(-theta), center)
                points[point_index] = tpoint

        if pressed_keys[pygame.K_n]:
            for point_index in range(0, len(points)):
                tpoint = rotate3D_Y(points[point_index], math.radians(theta), center)
                points[point_index] = tpoint

        if pressed_keys[pygame.K_m]:
            for point_index in range(0, len(points)):
                tpoint = rotate3D_Y(points[point_index], math.radians(-theta), center)
                points[point_index] = tpoint
                
        if state == State.DRAWING:
            if pygame.mouse.get_pressed()[0]:
                point = (pygame.mouse.get_pos()[0], 0, pygame.mouse.get_pos()[1])
                if not point in points:
                    points.append(point)

        screen.fill(background_color)
        draw_center_lines()
        display_start_msg()
        draw_points(points, drawing_color)
        pygame.display.update()
        # clock.tick(900)
            

pygame.init()
msg_font = pygame.font.SysFont("bahnschrift", 25)
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption('Rotate Drawing 3D')

main()