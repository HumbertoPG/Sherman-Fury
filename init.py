import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

screen_width = 1000
screen_height = 800
main_sphere_centerX = 150
main_sphere_centerZ = 150
main_sphere_radius = 12
white_sphere_center = [-50, 0, 50]
white_sphere_radius = 10

# Variables para definir la posicion del observador
EYE_X = 0.0
EYE_Y = 300.0
EYE_Z = 400.0
CENTER_X = 0
CENTER_Y = 0
CENTER_Z = 0
UP_X = 0
UP_Y = 1
UP_Z = 0

# Variables para dibujar los ejes del sistema
X_MIN = -500
X_MAX = 500
Y_MIN = -500
Y_MAX = 500
Z_MIN = -500
Z_MAX = 500

# Dimension del plano
DimBoard = 200

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
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, Y_MIN, 0.0)
    glVertex3f(0.0, Y_MAX, 0.0)
    glEnd()
    # Z axis in blue
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, Z_MIN)
    glVertex3f(0.0, 0.0, Z_MAX)
    glEnd()
    glLineWidth(1.0)

def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    
    pygame.display.set_caption("OpenGL: cubos")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, screen_width/screen_height, 0.01, 900.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
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

def draw_sphere(center, radius, slices=40, stacks=40):
    x, y, z = center
    sphere = gluNewQuadric()
    glPushMatrix()
    glTranslatef(x, y, z)
    gluSphere(sphere, radius, slices, stacks)
    glPopMatrix()
    gluDeleteQuadric(sphere)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    # Se dibuja el plano gris
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)
    draw_sphere(white_sphere_center, white_sphere_radius)
    glColor3f(0.0, 1.0, 0.2)
    draw_sphere([main_sphere_centerX, 0, main_sphere_centerZ], main_sphere_radius)

# Cambio: Función de verificación de colisiones
def check_collision(center1, radius1, center2, radius2):
    distance = math.sqrt((center1[0] - center2[0])**2 + (center1[2] - center2[2])**2)
    return distance <= (radius1 + radius2)

done = False
Init()

while not done:   
    keys = pygame.key.get_pressed()
    new_centerX = main_sphere_centerX
    new_centerZ = main_sphere_centerZ

    # Cambio: Verificación individual de colisión para cada dirección
    if keys[pygame.K_RIGHT] and main_sphere_centerX < 200:
        new_centerX += 1
        if not check_collision([new_centerX, 0, main_sphere_centerZ], main_sphere_radius, white_sphere_center, white_sphere_radius):
            main_sphere_centerX = new_centerX
    if keys[pygame.K_LEFT] and main_sphere_centerX > -200:
        new_centerX -= 1
        if not check_collision([new_centerX, 0, main_sphere_centerZ], main_sphere_radius, white_sphere_center, white_sphere_radius):
            main_sphere_centerX = new_centerX
    if keys[pygame.K_DOWN] and main_sphere_centerZ < 200:
        new_centerZ += 1
        if not check_collision([main_sphere_centerX, 0, new_centerZ], main_sphere_radius, white_sphere_center, white_sphere_radius):
            main_sphere_centerZ = new_centerZ
    if keys[pygame.K_UP] and main_sphere_centerZ > -200:
        new_centerZ -= 1
        if not check_collision([main_sphere_centerX, 0, new_centerZ], main_sphere_radius, white_sphere_center, white_sphere_radius):
            main_sphere_centerZ = new_centerZ

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    display()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
