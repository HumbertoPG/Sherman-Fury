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

def load_texture(image_path):
    texture_surface = pygame.image.load(image_path)
    texture_data = pygame.image.tostring(texture_surface, "RGB", True)
    width, height = texture_surface.get_size()
    
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    return texture_id

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
    
    global texture_ids
    texture_ids = {
        "front": load_texture('Img/Bosquefrente.png'),
        "left": load_texture('Img/Bosqueizq.png'),
        "right": load_texture('Img/Bosqueder.png'),
        "top": load_texture('Img/Bosquearriba.png'),
        "bottom": load_texture('Img/Bosquepiso.png')
    }

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
    height_offset = half_dim  # Offset to ensure the bottom is at the level of the blue axis

    vertices = {
        "front":  [(-half_dim, 0,  half_dim), ( half_dim, 0,  half_dim),
                   ( half_dim,  half_dim * 2,  half_dim), (-half_dim,  half_dim * 2,  half_dim)],
        "left":   [(-half_dim, 0, -half_dim), (-half_dim, 0,  half_dim),
                   (-half_dim,  half_dim * 2,  half_dim), (-half_dim,  half_dim * 2, -half_dim)],
        "right":  [( half_dim, 0,  half_dim), ( half_dim, 0, -half_dim),
                   ( half_dim,  half_dim * 2, -half_dim), ( half_dim,  half_dim * 2,  half_dim)],
        "top":    [(-half_dim,  half_dim * 2,  half_dim), ( half_dim,  half_dim * 2,  half_dim),
                   ( half_dim,  half_dim * 2, -half_dim), (-half_dim,  half_dim * 2, -half_dim)],
        "bottom": [(-half_dim, 0, -half_dim), ( half_dim, 0, -half_dim),
                   ( half_dim, 0,  half_dim), (-half_dim, 0,  half_dim)]
    }

    drawface(vertices["bottom"][0], vertices["bottom"][1], vertices["bottom"][2], vertices["bottom"][3], texture_ids["bottom"])
    drawface(vertices["front"][0], vertices["front"][1], vertices["front"][2], vertices["front"][3], texture_ids["front"])
    drawface(vertices["left"][0], vertices["left"][1], vertices["left"][2], vertices["left"][3], texture_ids["left"])
    drawface(vertices["right"][0], vertices["right"][1], vertices["right"][2], vertices["right"][3], texture_ids["right"])
    drawface(vertices["top"][0], vertices["top"][1], vertices["top"][2], vertices["top"][3], texture_ids["top"])

projectiles = []
tanks = []

def display():
    global projectiles
    global tanks

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    
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
    
    # Dibujar cubo texturizado
    CuboTexturizado()
    
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
