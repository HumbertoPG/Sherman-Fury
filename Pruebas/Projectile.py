from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

class Projectile:

    def __init__(self, x, y, z):

        self.flag = True

        self.x = x
        self.y = y
        self.z = z
        self.deg_sun = 0.0
        self.position = [0, 0, 0]

        self.v0 = 50
        self.angle_xy = 45
        self.angle_yz = 30
        self.t = 0.0
        self.dt = 1

    def draw(self):

        sphere = gluNewQuadric()

        angle_xy_rad = math.radians(self.angle_xy)
        angle_yz_rad = math.radians(self.angle_yz)
        
        # Componentes de la velocidad inicial
        v0x = self.v0 * math.cos(angle_yz_rad) * math.cos(angle_xy_rad)
        v0y = self.v0 * math.sin(angle_yz_rad)
        v0z = self.v0 * math.cos(angle_yz_rad) * math.sin(angle_xy_rad)
        
        # Calcular las posiciones en el tiempo t
        x_pos = v0x * self.t
        y_pos = v0y * self.t - 0.5 * 9.81 * self.t**2
        z_pos = v0z * self.t
        
        # return x_pos, y_pos, z_pos

        glPushMatrix()  # Guarda la matriz de transformación actual
        glTranslatef(x_pos, y_pos, z_pos)
        glColor3f(1.0, 0.0, 0.0)
        glRotatef(-90, 1.0, 0.0, 0.0)
        glScalef(2.0, 2.0, 2.0)
        glRotatef(self.deg_sun, 0.0, 0.0, 1.0)
        gluSphere(sphere, 30.0, 16, 16)
        self.deg_sun += 1.0
        if self.deg_sun >= 360.0:
            self.deg_sun = 0.0
        glPopMatrix()

        self.t += self.dt

        if (self.x == 0):
            flag = False

    def tiro_parabolico(self, v0, angle_xy, angle_yz, t, g=9.81):
    # Convertir ángulos de grados a radianes
        angle_xy_rad = math.radians(self.angle_xy)
        angle_yz_rad = math.radians(self.angle_yz)
        
        # Componentes de la velocidad inicial
        v0x = v0 * math.cos(angle_yz_rad) * math.cos(angle_xy_rad)
        v0y = v0 * math.sin(angle_yz_rad)
        v0z = v0 * math.cos(angle_yz_rad) * math.sin(angle_xy_rad)
        
        # Calcular las posiciones en el tiempo t
        x_pos = v0x * t
        y_pos = v0y * t - 0.5 * g * t**2
        z_pos = v0z * t
        
        return x_pos, y_pos, z_pos