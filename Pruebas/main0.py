import pygame
import math

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Tanque")

# Cargar imágenes
tank_cannon_img = pygame.image.load('tank_cannon.png').convert_alpha()
player_img = pygame.image.load('soldier.png').convert_alpha()

# Posición inicial del cañón y del personaje
tank_cannon_pos = (400, 300)  # Centro de la pantalla
player_pos = (tank_cannon_pos[0] - 20, tank_cannon_pos[1] + 30)  # Ajustar según el tamaño del cañón y del personaje

# Lista para guardar los disparos
bullets = []

# Velocidad del disparo
bullet_speed = 5

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener la posición del ratón
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calcular el ángulo del cañón
    rel_x, rel_y = mouse_x - tank_cannon_pos[0], mouse_y - tank_cannon_pos[1]
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

    # Dibujar fondo
    screen.fill((255, 255, 255))

    # Dibujar el cañón rotado
    rotated_cannon = pygame.transform.rotate(tank_cannon_img, angle)
    new_rect = rotated_cannon.get_rect(center=tank_cannon_pos)
    screen.blit(rotated_cannon, new_rect.topleft)

    # Dibujar al personaje
    screen.blit(player_img, player_pos)

    # Manejar disparos
    if pygame.mouse.get_pressed()[0]:
        bullet_x = tank_cannon_pos[0] + math.cos(math.radians(angle)) * 50
        bullet_y = tank_cannon_pos[1] - math.sin(math.radians(angle)) * 50
        bullets.append([bullet_x, bullet_y, angle])

    for bullet in bullets:
        bullet[0] += math.cos(math.radians(bullet[2])) * bullet_speed
        bullet[1] -= math.sin(math.radians(bullet[2])) * bullet_speed
        pygame.draw.circle(screen, (0, 0, 0), (int(bullet[0]), int(bullet[1])), 5)

    # Actualizar la pantalla
    pygame.display.flip()

# Salir del juego
pygame.quit()
