import random
import pygame
import math
from consts import *

pygame.init()
clock = pygame.time.Clock()

dis_width = 600
dis_height = 600

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("bahnschrift", 20)

def display_start_msg(dis):
    value = score_font.render("Draw with the mouse. When finished press ENTER once to", True, black)
    value2 = score_font.render("rotate 360 deg or SPACE bar multiple times to rotate manually", True, black)
    dis.blit(value, [25, dis_height / 2 - 30])
    dis.blit(value2, [25, dis_height / 2])

def display_second_msg(dis):
    value = score_font.render("use LEFT/RIGHT/UP/DOWN/N/M keys to rotate drawing", True, black)
    value2 = score_font.render("use 1/2/3/4/5/6/r keys to change color", True, black)
    dis.blit(value, [50, 20])
    dis.blit(value2, [110, 50])

# def sigmoid(x):
#     return int((5/(1+math.exp(-0.05*x)) + 2))

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

def rotate3D_Z(v,x,c):
    pos = [math.cos(x)*(v[0]-c[0]) + math.sin(x)*(v[1]-c[1]),-math.sin(x)*(v[0]-c[0]) + math.cos(x)*(v[1]-c[1]), v[2]]
    pos[0] = pos[0] + c[0]
    pos[1] = pos[1] + c[1]
    return pos

def rotate3D_Y(v,x,c):
    pos = [math.cos(x)*(v[0]-c[0]) + math.sin(x)*(v[2]-c[2]),v[1],-math.sin(x)*(v[0]-c[0]) + math.cos(x)*(v[2]-c[2])]
    pos[0] = pos[0] + c[0]
    pos[2] = pos[2] + c[2]
    return pos

def rotate3D_X(v,x,c):
    pos = [v[0],math.cos(x)*(v[1]-c[1]) + math.sin(x)*(v[2]-c[2]),-math.sin(x)*(v[1]-c[1]) + math.cos(x)*(v[2]-c[2])]
    pos[1] = pos[1] + c[1]
    pos[2] = pos[2] + c[2]
    return pos

def size(v):
    return realSigmoid(v[1])

def start():
    points = []
    center = (int(dis_width/2),0,int(dis_height/2))
    isDone = False
    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('rotate sandbox')
    dis.fill(white)
    display_start_msg(dis)
    pygame.display.update()
    isClosed = False
    isEnter = False
    color = red
    randomColor = False
    dis.fill(white)
    for i in range (dis_height):
        dis.set_at((center[0],i),black)
        dis.set_at((i,center[2]),black)
    while not isDone:
        if pygame.mouse.get_pressed()[0]:
            point = (pygame.mouse.get_pos()[0], 0, pygame.mouse.get_pos()[1])
            if not point in points:
                points.append(point)
                pygame.draw.rect(dis, color, [point[0], point[2], size(point), size(point)])
                pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == 13:
                    isDone = True
                    isEnter = True
                if event.key == pygame.K_SPACE:
                    isDone = True
                if event.key == pygame.K_1:
                    color = red
                if event.key == pygame.K_2:
                    color = blue
                if event.key == pygame.K_3:
                    color = green
                if event.key == pygame.K_4:
                    color = yellow
                if event.key == pygame.K_5:
                    color = purple
                if event.key == pygame.K_6:
                    color = black
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    length = len(points)
    if length < 20:
        dTheta = 1
        theta = 2
    else:
        dTheta = 10
        theta = 2
    isDone2 = False
    if isEnter:
        for i in range(int(360/dTheta)):
            for j in range(length):
                tpoint = rotate3D_Z(points[i * length + j], math.radians(-dTheta), center)
                points.append(tpoint)
                pygame.draw.rect(dis, color, [tpoint[0], tpoint[2], size(tpoint), size(tpoint)])
            pygame.display.update()
            clock.tick(int(-8.33 * dTheta + 108))
    else:
        i = 0
        while i < int(360/dTheta) and not isDone2:
            for event in pygame.event.get():
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[pygame.K_SPACE]:
                    display_second_msg(dis)
                    for j in range(0, length):
                        tpoint = rotate3D_Z(points[i * length + j], math.radians(-dTheta), center)
                        points.append(tpoint)
                        pygame.draw.rect(dis, color, [tpoint[0], tpoint[2], size(tpoint), size(tpoint)])
                    i += 1
                    pygame.display.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        isDone2 = True
                    if event.key == 13:
                        for k in range(int(360/dTheta) - i):
                            for m in range(length):
                                tpoint = rotate3D_Z(points[(i+k)*length + m], math.radians(-dTheta), center)
                                points.append(tpoint)
                                pygame.draw.rect(dis, color, [tpoint[0], tpoint[2], size(tpoint), size(tpoint)])
                            pygame.display.update()
                            clock.tick(int(-8.33 * dTheta + 108))
                        isDone2 = True

    display_second_msg(dis)
    pygame.display.update()
    while not isClosed:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            dis.fill(white)
            for j in range(0, len(points)):
                tpoint = rotate3D_Z(points[j], math.radians(-theta), center)
                points[j] = tpoint
                pygame.draw.rect(dis, color, [tpoint[0], tpoint[2], size(tpoint), size(tpoint)])
            pygame.display.update()
            # theta = min(theta+0.1, 30)
        elif pressed_keys[pygame.K_RIGHT]:
            dis.fill(white)
            for j in range(0, len(points)):
                tpoint = rotate3D_Z(points[j], math.radians(theta), center)
                points[j] = tpoint
                pygame.draw.rect(dis, color, [tpoint[0], tpoint[2], size(tpoint), size(tpoint)])
            pygame.display.update()
            # theta = min(theta+0.1, 30)
        elif pressed_keys[pygame.K_UP]:
            dis.fill(white)
            for j in range(0, len(points)):
                tpoint = rotate3D_X(points[j], math.radians(theta), center)
                points[j] = tpoint
                pygame.draw.rect(dis, color, [tpoint[0], tpoint[2], size(tpoint), size(tpoint)])
            pygame.display.update()
            # theta = min(theta+0.1, 30)
        elif pressed_keys[pygame.K_DOWN]:
            dis.fill(white)
            for j in range(0, len(points)):
                tpoint = rotate3D_X(points[j], math.radians(-theta), center)
                points[j] = tpoint
                pygame.draw.rect(dis, color, [tpoint[0], tpoint[2], size(tpoint), size(tpoint)])
            pygame.display.update()
            # theta = min(theta+0.1, 30)
        elif pressed_keys[pygame.K_n]:
            dis.fill(white)
            for j in range(0, len(points)):
                tpoint = rotate3D_Y(points[j], math.radians(theta), center)
                points[j] = tpoint
                pygame.draw.rect(dis, color, [tpoint[0], tpoint[2], size(tpoint), size(tpoint)])
            pygame.display.update()
            # theta = min(theta+0.1, 30)
        elif pressed_keys[pygame.K_m]:
            dis.fill(white)
            for j in range(0, len(points)):
                tpoint = rotate3D_Y(points[j], math.radians(-theta), center)
                points[j] = tpoint
                pygame.draw.rect(dis, color, [tpoint[0], tpoint[2], size(tpoint), size(tpoint)])
            pygame.display.update()
            # theta = min(theta+0.1, 30)
        else:
            theta = 1
        if randomColor:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    isClosed = True
                if event.key == pygame.K_r:
                    randomColor = not randomColor
                if event.key == pygame.K_1:
                    color = red
                if event.key == pygame.K_2:
                    color = blue
                if event.key == pygame.K_3:
                    color = green
                if event.key == pygame.K_4:
                    color = yellow
                if event.key == pygame.K_5:
                    color = purple
                if event.key == pygame.K_6:
                    color = black
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

start()