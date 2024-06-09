import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from objloadTank import OBJ

screen_width = 1000
screen_height = 800
FOVY = 60.0
ZNEAR = 0.01
ZFAR = 900.0

# Posición de la cámara más cercana
EYE_X = 150.0
EYE_Y = 100.0
EYE_Z = 150.0

CENTER_X = 0
CENTER_Y = 0
CENTER_Z = 0
UP_X = 0
UP_Y = 1
UP_Z = 0

DimBoard = 200

theta = 0.0
radius = 10  # Ajuste del radio más cercano

pygame.init()

objetos = []

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(-500, 0.0, 0.0)
    glVertex3f(500, 0.0, 0.0)
    glEnd()
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, -500, 0.0)
    glVertex3f(0.0, 500, 0.0)
    glEnd()
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, -500)
    glVertex3f(0.0, 0.0, 500)
    glEnd()
    glLineWidth(1.0)

def Init():
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glLightfv(GL_LIGHT0, GL_POSITION, (0, 200, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.5, 0.5, 0.5, 1.0))

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)
    
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 200, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.5, 0.5, 0.5, 1.0))

    glClearColor(0.93, 0.86, 0.76, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    try:
        obj = OBJ("Sherman-Fury/T72Tank.obj", swapyz=True)
        objetos.append(obj)
        print("Object appended to list successfully.")
    except Exception as e:
        print(f"Error initializing object: {e}")

    print(f"Number of objects loaded: {len(objetos)}")

def lookat():
    global EYE_X, EYE_Z, radius
    radius = 150  # Ajusta este valor para acercar o alejar la cámara
    EYE_X = radius * (math.cos(math.radians(theta)) + math.sin(math.radians(theta)))
    EYE_Z = radius * (-math.sin(math.radians(theta)) + math.cos(math.radians(theta)))
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

def displayobj():
    glPushMatrix()
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(0.0, 0.0, 30.0)  # Ajusta estos valores según sea necesario
    glScale(4.0, 4.0, 4.0)  # Ajusta estos valores según sea necesario para hacer el objeto más grande
    for obj in objetos:
        obj.render()
    glPopMatrix()

def display():
    global theta, radius
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    radius = 150  # Ajusta este valor para acercar o alejar la cámara
    gluLookAt(radius * math.cos(math.radians(theta)), EYE_Y, radius * math.sin(math.radians(theta)),
              CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

    Axis()
    displayobj()
    pygame.display.flip()

def main():
    global theta, radius
    done = False
    Init()
    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            if theta > 359.0:
                theta = 0
            else:
                theta += 1.0
            lookat()

        if keys[pygame.K_LEFT]:
            if theta < 1.0:
                theta = 360.0
            else:
                theta -= 1.0
            lookat()

        display()
        clock.tick(60)  # Limita el bucle a 60 FPS

if __name__ == "__main__":
    main()
    pygame.quit()
