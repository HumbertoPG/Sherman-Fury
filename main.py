import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import sys

from Cubo import Cubo
from objloader import *

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

objetos = []

newCubo = Cubo(DimBoard, 0, 0, DimBoard, 1)
newNewCubo = Cubo(DimBoard, -(DimBoard / 2), 0, DimBoard, 1)

EYE_X = 300.0
EYE_Y = 200.0
EYE_Z = 300.0
CENTER_X = 0
CENTER_Y = 0
CENTER_Z = 0
UP_X=0
UP_Y=1
UP_Z=0

angle_pitch = 0
angle_yaw = 0

pygame.init()

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    # X axis in red
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN, 0.0, 0.0)
    glVertex3f(X_MAX, 0.0, 0.0)
    glEnd()
    # Y axis in green
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, Y_MIN, 0.0)
    glVertex3f(0.0, Y_MAX, 0.0)
    glEnd()
    # Z axis in blue
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, Z_MIN)
    glVertex3f(0.0, 0.0, Z_MAX)
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
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 200, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)  # most obj files expect to be smooth-shaded
    objetos.append(OBJ("14077_WWII_Tank_Germany_Panzer_III_v1_L2.obj", swapyz=True))
    objetos[0].generate()


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


def displayobj():
    glPushMatrix()
    # correcciones para dibujar el objeto en plano XZ
    # esto depende de cada objeto
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(0.0, 0.0, 15.0)
    glScale(10.0, 10.0, 10.0)
    objetos[0].render()
    glPopMatrix()


def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)  # (-x, y, -z)
    glVertex3d(-DimBoard, 0, DimBoard)  # ()
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()

    newCubo.draw()
    newCubo.update()

    newNewCubo.draw()
    newNewCubo.update()

    displayobj()


def update_camera():
    global posX, posY, posZ, viewX, viewY, viewZ
    viewX = posX + math.sin(math.radians(angle_yaw))
    viewZ = posZ + math.cos(math.radians(angle_yaw))
    viewY = posY + math.sin(math.radians(angle_pitch))
    glLoadIdentity()
    gluLookAt(posX, posY, posZ,  # Posición de la cámara
              viewX, viewY, viewZ,  # Punto al que la cámara está mirando
              0, 1, 0)


done = False

Init()

while not done:

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle_yaw -= 1
        update_camera()
    if keys[pygame.K_RIGHT]:
        angle_yaw += 1
        update_camera()

    if keys[pygame.K_UP]:
        angle_pitch += 1
        update_camera()

    if keys[pygame.K_DOWN]:
        angle_pitch -= 1
        update_camera()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

    display()

    pygame.display.flip()
    pygame.time.wait(5)

pygame.quit()
