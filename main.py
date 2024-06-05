import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

screen_width, screen_height = 0, 0  

FOVY = 55.0
ZNEAR = 0.1
ZFAR = 1000.0

DimBoard = 546

CAMERA_Y_MIN = 0
CAMERA_Y_MAX = 100
CAMERA_Z_MIN = -300
CAMERA_Z_MAX = -100

posX = 0
posY = DimBoard / 2
posZ = -DimBoard

viewX = 0
viewY = DimBoard / 2
viewZ = 0

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
    global screen_width, screen_height
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.DOUBLEBUF | pygame.OPENGL | pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()  # Obtener el tamaño de la pantalla
    pygame.display.set_caption("SHERMAN-FURY")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(posX, posY + 20, posZ - 150,  # Posición inicial de la cámara
              viewX, viewY, viewZ,  # Punto al que la cámara está mirando
              0, 1, 0)

    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
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

    vertices = {
        "front":  [(-half_dim, -half_dim,  half_dim), ( half_dim, -half_dim,  half_dim),
                   ( half_dim,  half_dim,  half_dim), (-half_dim,  half_dim,  half_dim)],
        "left":   [(-half_dim, -half_dim, -half_dim), (-half_dim, -half_dim,  half_dim),
                   (-half_dim,  half_dim,  half_dim), (-half_dim,  half_dim, -half_dim)],
        "right":  [( half_dim, -half_dim,  half_dim), ( half_dim, -half_dim, -half_dim),
                   ( half_dim,  half_dim, -half_dim), ( half_dim,  half_dim,  half_dim)],
        "top":    [(-half_dim,  half_dim,  half_dim), ( half_dim,  half_dim,  half_dim),
                   ( half_dim,  half_dim, -half_dim), (-half_dim,  half_dim, -half_dim)],
        "bottom": [(-half_dim, -half_dim, -half_dim), ( half_dim, -half_dim, -half_dim),
                   ( half_dim, -half_dim,  half_dim), (-half_dim, -half_dim,  half_dim)]
    }

    drawface(vertices["front"][0], vertices["front"][1], vertices["front"][2], vertices["front"][3], texture_ids["front"])
    drawface(vertices["left"][0], vertices["left"][1], vertices["left"][2], vertices["left"][3], texture_ids["left"])
    drawface(vertices["right"][0], vertices["right"][1], vertices["right"][2], vertices["right"][3], texture_ids["right"])
    drawface(vertices["top"][0], vertices["top"][1], vertices["top"][2], vertices["top"][3], texture_ids["top"])
    drawface(vertices["bottom"][0], vertices["bottom"][1], vertices["bottom"][2], vertices["bottom"][3], texture_ids["bottom"])

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    CuboTexturizado()
    
    pygame.display.flip()

done = False

Init()

while not done:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        posX += 1
        viewX += 1
    if keys[pygame.K_RIGHT]:
        posX -= 1
        viewX -= 1
    if keys[pygame.K_UP]:
        viewY = max(CAMERA_Y_MIN, viewY - 1)
        posY = max(CAMERA_Y_MIN, posY - 1)
    if keys[pygame.K_DOWN]:
        viewY = min(CAMERA_Y_MAX, viewY + 1)
        posY = min(CAMERA_Y_MAX, posY + 1)
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
    
    posZ = max(CAMERA_Z_MIN, min(CAMERA_Z_MAX, posZ))
    
    glLoadIdentity()
    gluLookAt(posX, posY, posZ,  # Posición de la cámara
              viewX, viewY, viewZ,  # Punto al que la cámara está mirando
              0, 1, 0)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    display()
    pygame.time.wait(5)

pygame.quit()
