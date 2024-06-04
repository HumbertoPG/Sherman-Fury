import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import sys

from Cubo import Cubo

screen_width = 546
screen_height = 546

FOVY = 55.0
ZNEAR = 0.1
ZFAR = 1000.0

DimBoard = 546

X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500

posX = 0
posY = DimBoard/2
posZ = -DimBoard

viewX = 0
viewY = DimBoard/2
viewZ = 0

newCubo = Cubo(DimBoard, 0, 0, DimBoard, 1)
newNewCubo = Cubo(DimBoard, -(DimBoard / 2), 0, DimBoard, 1)

pygame.init()

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)


def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: Juego")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(posX, posY, posZ,  # Posición de la cámara
          viewX, viewY, viewZ,  # Punto al que la cámara está mirando
          0, 1, 0)

    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    
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

def display():
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Axis()
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard) # (-x, y, -z)
    glVertex3d(-DimBoard, 0, DimBoard) #()
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()

    newCubo.draw()
    newCubo.update()

    newNewCubo.draw()
    newNewCubo.update()

done = False

Init()

while not done:

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
            posX += 1
            viewX += 1
            glLoadIdentity()
            gluLookAt(posX, posY, posZ,  # Posición de la cámara
          viewX, viewY, viewZ,  # Punto al que la cámara está mirando
          0, 1, 0)
    if keys[pygame.K_RIGHT]:
            posX -= 1
            viewX -= 1
            glLoadIdentity()
            gluLookAt(posX, posY, posZ,  # Posición de la cámara
          viewX, viewY, viewZ,  # Punto al que la cámara está mirando
          0, 1, 0)
    
    if keys[pygame.K_UP]:
            viewY -= 1
            glLoadIdentity()
            gluLookAt(posX, posY, posZ,  # Posición de la cámara
          viewX, viewY, viewZ,  # Punto al que la cámara está mirando
          0, 1, 0)
    
    if keys[pygame.K_DOWN]:
            viewY += 1
            glLoadIdentity()
            gluLookAt(posX, posY, posZ,  # Posición de la cámara
          viewX, viewY, viewZ,  # Punto al que la cámara está mirando
          0, 1, 0) 
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            done = True
            
    display()
    
    pygame.display.flip()
    pygame.time.wait(5)

pygame.quit()