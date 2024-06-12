from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

class Projectile:
    
    def __init__(self, x, y, z, angleYZ):
        
        self.flag = True

        self.x_pos = x
        self.y_pos = y
        self.z_pos = z
        self.deg_sun = 0.0
        self.position = [0, 0, 0]

        self.v0 = 100  # Velocidad inicial
        self.angle_yz = angleYZ  # Ángulo en el plano YZ
        self.t = 0.0
        self.dt = 0.1  # Pequeño intervalo de tiempo para la animación

    def draw(self):
        
        if self.flag:
        
            sphere = gluNewQuadric()

            angle_yz_rad = math.radians(self.angle_yz)

            # Componentes de la velocidad inicial
            v0y = self.v0 * math.sin(angle_yz_rad)
            v0z = self.v0 * math.cos(angle_yz_rad)

            # Calcular las posiciones en el tiempo t
            self.y_pos = v0y * self.t - 0.5 * 9.81 * self.t**2
            self.z_pos = v0z * self.t

            glPushMatrix()  # Guarda la matriz de transformación actual
            glTranslatef(self.x_pos, self.y_pos, self.z_pos)
            glColor3f(0.7, 0.7, 0.7)
            glRotatef(-90, 1.0, 0.0, 0.0)
            glScalef(2.0, 2.0, 2.0)
            glRotatef(self.deg_sun, 0.0, 0.0, 1.0)
            gluSphere(sphere, 1.0, 16, 16)
            self.deg_sun += 1.0
            if self.deg_sun >= 360.0:
                self.deg_sun = 0.0
            glPopMatrix()

            self.t += self.dt

            if self.y_pos < 0:
                self.flag = False