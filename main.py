import os
import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

import sys
sys.path.append('..')

# Import obj loader
from objectloader import *
from Projectile import *

screen_width = 1200
screen_height = 800
FOVY = 60.0
ZNEAR = 0.01
ZFAR = 2000.0
EYE_X = 4.0
EYE_Y = 7.0
EYE_Z = 5.0
CENTER_X = 4.0
CENTER_Y = 0.0
CENTER_Z = 300.0
UP_X = 0.0
UP_Y = 1.0
UP_Z = 0.0
X_MIN = -500
X_MAX = 500
Y_MIN = -500
Y_MAX = 500
Z_MIN = -500
Z_MAX = 500
DimBoard = 600
distance1 = 0
distance2 = 0
distance3 = 0
flag1 = True
flag2 = True
flag3 = True
displacement1= -90.0
displacement2= -110.0
displacement3= -130.0

objetos = []
proyectiles = []

theta = 0.0
radius = 300

shotAngleYZ = 23

textures = []

filename1 = "pruebas-generales/sky.jpg"

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

def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image, "RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)

def draw_skybox():
    glDisable(GL_DEPTH_TEST)  # Disable depth testing so skybox is always in the background
    size = 600.0  # Skybox size
    
    glColor3f(1.0, 1.0, 1.0)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[0])
    
    glBegin(GL_QUADS)
    # Front face
    glTexCoord2f(0.0, 0.0); glVertex3f(-size, -size, -size)
    glTexCoord2f(1.0, 0.0); glVertex3f(size, -size, -size)
    glTexCoord2f(1.0, 1.0); glVertex3f(size, size, -size)
    glTexCoord2f(0.0, 1.0); glVertex3f(-size, size, -size)
    glEnd()

    glBegin(GL_QUADS)
    # Back face
    glTexCoord2f(0.0, 0.0); glVertex3f(size, -size, size)
    glTexCoord2f(1.0, 0.0); glVertex3f(-size, -size, size)
    glTexCoord2f(1.0, 1.0); glVertex3f(-size, size, size)
    glTexCoord2f(0.0, 1.0); glVertex3f(size, size, size)
    glEnd()

    glBegin(GL_QUADS)
    # Left face
    glTexCoord2f(0.0, 0.0); glVertex3f(-size, -size, size)
    glTexCoord2f(1.0, 0.0); glVertex3f(-size, -size, -size)
    glTexCoord2f(1.0, 1.0); glVertex3f(-size, size, -size)
    glTexCoord2f(0.0, 1.0); glVertex3f(-size, size, size)
    glEnd()

    glBegin(GL_QUADS)
    # Right face
    glTexCoord2f(0.0, 0.0); glVertex3f(size, -size, -size)
    glTexCoord2f(1.0, 0.0); glVertex3f(size, -size, size)
    glTexCoord2f(1.0, 1.0); glVertex3f(size, size, size)
    glTexCoord2f(0.0, 1.0); glVertex3f(size, size, -size)
    glEnd()

    glBegin(GL_QUADS)
    
    # Top face
    glTexCoord2f(0.0, 0.0); glVertex3f(-size, size, -size)
    glTexCoord2f(1.0, 0.0); glVertex3f(size, size, -size)
    glTexCoord2f(1.0, 1.0); glVertex3f(size, size, size)
    glTexCoord2f(0.0, 1.0); glVertex3f(-size, size, size)
    glEnd()

    glDisable(GL_TEXTURE_2D)

    glEnable(GL_DEPTH_TEST)  # Re-enable depth testing

def Init():
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT, GL_FILL)

    Texturas(filename1)  # Asegúrate de que tienes un archivo llamado sky.jpg en tu directorio

    glLightfv(GL_LIGHT0, GL_POSITION, (0, 200, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)  # most obj files expect to be smooth-shaded
    objetos.append(OBJ("pruebas-generales/Vivianna_Corporate_Park.obj", swapyz=True))
    objetos[0].generate()
    objetos.append(OBJ("pruebas-generales/T72Tank.obj", swapyz=True))
    objetos[1].generate()
    objetos.append(OBJ("pruebas-generales/T72TankEnemy.obj", swapyz = True))
    objetos.append(OBJ("pruebas-generales/T72TankEnemy.obj", swapyz = True))
    objetos.append(OBJ("pruebas-generales/T72TankEnemy.obj", swapyz = True))
    objetos.append(OBJ("pruebas-generales/T72TankEnemy.obj", swapyz = True))
    

def lookat():
    global EYE_X
    global EYE_Z
    global radius
    EYE_X = radius * (math.cos(math.radians(theta)) + math.sin(math.radians(theta)))
    EYE_Z = radius * (-math.sin(math.radians(theta)) + math.cos(math.radians(theta)))
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

def displayScenario():
    glPushMatrix()
    # Correcciones para dibujar el objeto en plano XZ
    # Esto depende de cada objeto
    glColor3f(0.2, 0.2, 0.2)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glRotatef(45.0, 0.0, 0.0, 1.0)
    glTranslatef(-275.0, 200.0, 5.0)
    glScale(0.015, 0.015, 0.015)
    objetos[0].render()
    glPopMatrix()

def displayMain():
    glPushMatrix()
    glColor3f(0.3, 0.3, 0.3)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(4.0, 0.0, 6.0)
    glRotatef(180.0, 0.0, 0.0, 1.0)
    glScale(0.5, 0.5, 0.5)
    objetos[1].render()
    glPopMatrix()
    
    
def displayEnemies():
    if flag1 == True:
        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glTranslatef(4.0, displacement1 + distance1 , 6.0)
        glScale(0.5, 0.5, 0.5)
        objetos[2].render()
        glPopMatrix()
    if flag2 == True:
        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glTranslatef(8.0, displacement2 + distance2, 6.0)
        glScale(0.5, 0.5, 0.5)
        objetos[3].render()
        glPopMatrix()
    if flag3 == True:
        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glTranslatef(0.0, displacement3 + distance3, 6.0)
        glScale(0.5, 0.5, 0.5)
        objetos[4].render()
        glPopMatrix()
    

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_skybox()  # Dibuja el skybox antes de los demás objetos
    Axis()
    # Se dibuja el plano gris
    glColor3f(0.0, 0.3, 0.7)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()

    displayScenario()
    displayMain()  
    displayEnemies()
    
    for proyectil in proyectiles:
        proyectil.draw()



done = False
Init() 
while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_SPACE:
                proyectiles.append(Projectile(EYE_X, EYE_Y, EYE_Z, shotAngleYZ))
                
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] and shotAngleYZ > 0:
        shotAngleYZ -= 1
    if keys[pygame.K_UP] and shotAngleYZ < 23:
        shotAngleYZ += 1

    # avanzar observador
    if keys[pygame.K_d]:
        if EYE_X > -0.4:
            EYE_X -= 0.06
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

    elif keys[pygame.K_a]:
        if EYE_X < 8.4:
            EYE_X += 0.06
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

    elif keys[pygame.K_s]:
        if EYE_Z > 2.0:
            EYE_Z -= 0.06
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

    elif keys[pygame.K_w]:
        if EYE_Z < 200.0:
            EYE_Z += 0.06
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

    distance1 +=1
    distance2 +=1
    distance3 +=1
    
    if displacement1 + distance1 == -10:
        flag1 = False
    if displacement2 + distance2 == -10:
        flag2 = False
    if displacement3 + distance3 == -10:
        flag3 = False
        
    
    display()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()