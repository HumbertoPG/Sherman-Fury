import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import sys

screen_width = 1280
screen_height = 720

DimBoard = 5000

xPos = 0
yPos = 250
zPos = 0

xView = 0
yView = 250
zView = 250

from Projectile import Projectile
from Tank import Tank

pygame.init()

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    # X axis in red
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(-DimBoard, 0.0, 0.0)
    glVertex3f(DimBoard, 0.0, 0.0)
    glEnd()
    # Y axis in green
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, -DimBoard, 0.0)
    glVertex3f(0.0, DimBoard, 0.0)
    glEnd()
    # Z axis in blue
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, -DimBoard)
    glVertex3f(0.0, 0.0, DimBoard)
    glEnd()
    glLineWidth(1.0)

def Init():
    
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Sherman Fury")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, screen_width/screen_height, 0.1, 1000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(xPos, yPos, zPos,  # Posición de la cámara
              xView, yView, zView,  # Punto al que la cámara está mirando
              0, 1, 0)  # Vector Up
    
    # gluLookAt(-500, 250, 0,  # Posición de la cámara
    #           0, 0, 0,  # Punto al que la cámara está mirando
    #           1, 0, 0)  # Vector Up
    
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 200, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)
    

def PlanoTexturizado():
    
    glColor3f(1, 1, 1)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(0, 0, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(0, DimBoard, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(DimBoard, DimBoard, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(DimBoard, 0, 0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

projectiles = []
tanks = []

def display():
    
    global projectiles
    global tanks

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()
    
    tmp = []
    tmpTank = []

    for proyectil in projectiles:
        proyectil.draw()
        if proyectil.flag != False:
            tmp.append(proyectil)
    
    for tank in tanks:
        tank.display()
        tank.update()
        if tank.flag != False:
            tmpTank.append(tank)
    
    projectiles = tmp
    tanks = tmpTank
    
    # print(len(projectiles))
    print(len(tanks))
    
    
    

Init()

done = False

shotAngleYZ = 0

while not done:

    display()

    pygame.display.flip()
    pygame.time.wait(50)

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                projectiles.append(Projectile(xPos, 250, yPos, shotAngleYZ))
                tanks.append(Tank("Chevrolet_Camaro_SS_Low.obj", 0.0, -500.0, 15.0))
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        xPos += 1
        xView += 1
        glLoadIdentity()
        gluLookAt(xPos, yPos, zPos,  # Posición de la cámara
              xView, yView, zView,  # Punto al que la cámara está mirando
              0, 1, 0)  # Vector Up
    if keys[pygame.K_RIGHT]:
        xPos -= 1
        xView -= 1
        glLoadIdentity()
        gluLookAt(xPos, yPos, zPos,  # Posición de la cámara
              xView, yView, zView,  # Punto al que la cámara está mirando
              0, 1, 0)  # Vector Up
    if keys[pygame.K_UP]:
        yView += 1
        shotAngleYZ += 1
        glLoadIdentity()
        gluLookAt(xPos, yPos, zPos,  # Posición de la cámara
              xView, yView, zView,  # Punto al que la cámara está mirando
              0, 1, 0)  # Vector Up
    if keys[pygame.K_DOWN]:
        yView -= 1
        shotAngleYZ -= 1
        glLoadIdentity()
        gluLookAt(xPos, yPos, zPos,  # Posición de la cámara
              xView, yView, zView,  # Punto al que la cámara está mirando
              0, 1, 0)  # Vector Up

pygame.quit()
