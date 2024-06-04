import math
import numpy as np
import matplotlib.pyplot as plt

def tiro_parabolico(v0, angle_xy, angle_yz, g=9.81, t_total=10, dt=0.01):

    angle_xy_rad = math.radians(angle_xy)
    angle_yz_rad = math.radians(angle_yz)
    
    v0x = v0 * math.cos(angle_yz_rad) * math.cos(angle_xy_rad)
    v0y = v0 * math.sin(angle_yz_rad)
    v0z = v0 * math.cos(angle_yz_rad) * math.sin(angle_xy_rad)
    
    x = []
    y = []
    z = []
    
    x_pos = 0
    y_pos = 0
    z_pos = 0
    
    t = 0
    
    while t <= t_total:
        # Posiciones en cada instante de tiempo
        x_pos = v0x * t
        y_pos = v0y * t - 0.5 * g * t**2
        z_pos = v0z * t
        
        if y_pos < 0:
            break
        
        # Almacenar posiciones
        x.append(x_pos)
        y.append(y_pos)
        z.append(z_pos)
        
        # Incrementar el tiempo
        t += dt
    
    return x, y, z