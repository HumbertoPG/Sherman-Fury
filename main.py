import os
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import sys
sys.path.append('..')
from objectloader import *
from Projectile import *

screen_width = 1200
screen_height = 800
FOVY = 60.0
ZNEAR = 0.01
ZFAR = 600.0
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
speed1 = 0.3
speed2 = 0.3
speed3 = 0.3
displacement1 = -170.0
displacement2 = -170.0
displacement3 = -170.0
player_health = 100
score = 0  # Variable para el puntaje

objetos = []
proyectiles = []

theta = 0.0
radius = 300

shotAngleYZ = 23

textures = []
filename1 = "sky.jpg"
move_sound_file = "move_sound.mp3"
explosion_sound_file = "explosion.mp3"

pygame.init()
pygame.mixer.init()
move_sound = pygame.mixer.Sound(move_sound_file)
move_sound_channel = pygame.mixer.Channel(0)
explosion_sound = pygame.mixer.Sound(explosion_sound_file)


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
    glDisable(GL_DEPTH_TEST)
    size = 600.0

    glColor3f(1.0, 1.0, 1.0)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[0])

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-size, -size, -size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(size, -size, -size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(size, size, -size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-size, size, -size)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(size, -size, size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-size, -size, size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-size, size, size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(size, size, size)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-size, -size, size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-size, -size, -size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-size, size, -size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-size, size, size)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(size, -size, -size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(size, -size, size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(size, size, size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(size, size, -size)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-size, size, -size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(size, size, -size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(size, size, size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-size, size, size)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)


def Init():
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Sherman Fury")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT, GL_FILL)

    Texturas(filename1)

    glLightfv(GL_LIGHT0, GL_POSITION, (0, 200, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)
    objetos.append(OBJ("Vivianna_Corporate_Park.obj", swapyz=True))
    objetos[0].generate()
#    objetos.append(OBJ("T72Tank.obj", swapyz=True))
#    objetos[1].generate()
    objetos.append(OBJ("T72TankEnemy.obj", swapyz=True))
    objetos[1].generate()
    objetos.append(OBJ("T72TankEnemy.obj", swapyz=True))
    objetos[2].generate()
    objetos.append(OBJ("T72TankEnemy.obj", swapyz=True))
    objetos[3].generate()
    objetos.append(OBJ("T72TankEnemy.obj", swapyz=True))


def lookat():
    global EYE_X
    global EYE_Z
    global radius
    EYE_X = radius * (math.cos(math.radians(theta)) + math.sin(math.radians(theta)))
    EYE_Z = radius * (-math.sin(math.radians(theta)) + math.cos(math.radians(theta)))
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)


def decay_player_health():
    global player_health
    if player_health == 100:
        player_health = 75
    elif player_health == 75:
        player_health = 50
    elif player_health == 50:
        player_health = 25
    else:
        player_health = 0


def draw_health_triangle(health):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, screen_width, 0, screen_height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    size = 50
    x = screen_width - size - 70
    y = size + 90

    if health == 100:
        glColor3f(0.0, 1.0, 0.0)
    elif health == 75:
        glColor3f(1.0, 1.0, 0.0)
    elif health == 50:
        glColor3f(1.0, 0.5, 0.0)
    elif health == 25:
        glColor3f(1.0, 0.0, 0.0)
    else:
        glColor3f(0.5, 0.5, 0.5)

    glBegin(GL_TRIANGLES)
    glVertex2f(x, y + size)
    glVertex2f(x - size, y - size)
    glVertex2f(x + size, y - size)
    glEnd()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

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




def displayEnemies():
    if flag1:
        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glTranslatef(4.0, displacement1 + distance1, 6.0)
        glScale(0.5, 0.5, 0.5)
        objetos[2].render()
        glPopMatrix()
    if flag2:
        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glTranslatef(8.0, displacement2 + distance2, 6.0)
        glScale(0.5, 0.5, 0.5)
        objetos[3].render()
        glPopMatrix()
    if flag3:
        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glTranslatef(0.0, displacement3 + distance3, 6.0)
        glScale(0.5, 0.5, 0.5)
        objetos[4].render()
        glPopMatrix()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_skybox()
    glColor3f(0.0, 0.3, 0.7)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()

    displayScenario()
    displayEnemies()

    for proyectil in proyectiles:
        proyectil.draw()
        check_collision(proyectil)a
        if proyectil.y_pos < 0 or proyectil.z_pos > 600:
            proyectiles.remove(proyectil)

    draw_health_triangle(player_health)


def check_collision(proyectil):
    global flag1, flag2, flag3, score
    if flag1:
        if check_proyectil_collision_with_enemy(proyectil, 4.0, displacement1 + distance1, 6.0, 2):
            flag1 = False
            explosion_sound.play()
            score += 100
    if flag2:
        if check_proyectil_collision_with_enemy(proyectil, 8.0, displacement2 + distance2, 6.0, 1):
            flag2 = False
            explosion_sound.play()
            score += 10
    if flag3:
        if check_proyectil_collision_with_enemy(proyectil, 0.0, displacement3 + distance3, 6.0, 3):
            flag3 = False
            explosion_sound.play()
            score += 100


def check_proyectil_collision_with_enemy(proyectil, enemy_x, enemy_y, enemy_z, tank):
    distance = math.sqrt((proyectil.x_pos - enemy_x) ** 2 + (proyectil.z_pos - (-1 * enemy_y)) ** 2 + (proyectil.y_pos - enemy_z) ** 2)
    return distance < proyectil.radius + 2


def reset_enemy(enemy_flag, enemy_distance, speed):
    enemy_flag = True
    enemy_distance = 0
    speed += 0.3
    pygame.time.wait(500)
    return enemy_flag, enemy_distance, speed


def game_over():
    print("Gracias por jugar Sherman Fury")
    print(f"Puntaje obtenido: {score}")
    pygame.quit()
    sys.exit()


done = False
Init()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over()
                done = True
            if event.key == pygame.K_SPACE:
                proyectiles.append(Projectile(EYE_X, EYE_Y, EYE_Z, shotAngleYZ))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] and shotAngleYZ > -3:
        shotAngleYZ -= 4
    if keys[pygame.K_UP] and shotAngleYZ < 25:
        shotAngleYZ += 4

    if keys[pygame.K_d]:
        if EYE_X > -0.4:
            EYE_X -= 0.3
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
        if not move_sound_channel.get_busy():
            move_sound_channel.play(move_sound, loops=-1)

    elif keys[pygame.K_a]:
        if EYE_X < 8.4:
            EYE_X += 0.3
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
        if not move_sound_channel.get_busy():
            move_sound_channel.play(move_sound, loops=-1)
    else:
        move_sound_channel.stop()

    if not flag1:
        flag1, distance1, speed1 = reset_enemy(flag1, distance1, speed1)
    if not flag2:
        flag2, distance2, speed2 = reset_enemy(flag2, distance2, speed2)
    if not flag3:
        flag3, distance3, speed3 = reset_enemy(flag3, distance3, speed3)

    distance1 += speed1
    distance2 += speed2
    distance3 += speed3

    if displacement1 + distance1 > -10:
        if flag1:
            decay_player_health()
            flag1 = False
    if displacement2 + distance2 > -10:
        if flag2:
            decay_player_health()
            flag2 = False
    if displacement3 + distance3 > -10:
        if flag3:
            decay_player_health()
            flag3 = False

    display()

    if player_health <= 0:
        game_over()
        done = True

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
