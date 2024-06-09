import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import random
import math

from objloader import *

class Tank:
     
    def __init__(self, obj_file, x, y, z, scale=10.0, rotation=(-90.0, 1.0, 0.0, 0.0)):

        self.flag = True

        self.obj = OBJ(obj_file, swapyz=True)
        self.scale = scale
        self.posX = x
        self.posY = y
        self.posZ = z
        self.rotation = rotation
        self.obj.generate()
    
    def display(self):
        
        glPushMatrix()
        glRotatef(*self.rotation)
        glTranslatef(self.posX, self.posY, self.posZ)
        glScale(self.scale, self.scale, self.scale)
        self.obj.render()
        glPopMatrix()
    
    def update(self):
        
        self.posY += 10
        
        if self.posY > 100:
            self.flag = False