import pygame
import sys

pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VaStar - Visualizador A*")

clock = pygame.time.Clock()

# Fuente robótica
font = pygame.font.Font("PressStart2P-Regular.ttf", 32)

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((200, 200, 200))

    # PANEL PRINCIPAL
    text_main = font.render("Introduce un tamaño", True, (0, 255, 180))

    screen.blit(text_main, (20, 20))

    pygame.display.flip()
pygame.quit()
sys.exit()