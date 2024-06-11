import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import sys

screen_width = 1280
screen_height = 720
DimBoard = 500

xPos = 0
yPos = 250
zPos = 0
xView = 0
yView = 250
zView = 250

from Projectile import Projectile

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
    gluLookAt(xPos, yPos, zPos, xView, yView, zView, 0, 1, 0)
    
    glClearColor(0.5, 0.5, 0.5, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 200, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)
def CuboTexturizado():
    glColor3f(1, 1, 1)
    
    def drawface(v0, v1, v2, v3, texture_id):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)
    
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(*v0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(*v1)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(*v2)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(*v3)
        glEnd()
    
        glDisable(GL_TEXTURE_2D)

    half_dim = DimBoard / 2

projectiles = []

def display():
    
    global projectiles

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    
    tmp = []

    for proyectil in projectiles:
        proyectil.draw()
        if proyectil.flag != False:
            tmp.append(proyectil)
    
    projectiles = tmp
    
    # print(len(projectiles))
    

Init()

done = False

shotAngleYZ = 45

while not done:
    
    display()
    
    pygame.display.flip()
    pygame.time.wait(50)

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                projectiles.append(Projectile(xPos, yPos, zPos, shotAngleYZ))
                
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        xPos += 1
        xView += 1
        glLoadIdentity()
        gluLookAt(xPos, yPos, zPos, xView, yView, zView, 0, 1, 0)
    if keys[pygame.K_RIGHT]:
        xPos -= 1
        xView -= 1
        glLoadIdentity()
        gluLookAt(xPos, yPos, zPos, xView, yView, zView, 0, 1, 0)
    if keys[pygame.K_UP]:
        yView += 1
        shotAngleYZ += 1
        glLoadIdentity()
        gluLookAt(xPos, yPos, zPos, xView, yView, zView, 0, 1, 0)
    if keys[pygame.K_DOWN]:
        yView -= 1
        shotAngleYZ -= 1
        glLoadIdentity()
        gluLookAt(xPos, yPos, zPos, xView, yView, zView, 0, 1, 0)
        
pygame.quit()
