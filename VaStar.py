import pygame
import sys

from screens.menu_screen import MenuScreen
from screens.game_screen import GameScreen

pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VaStar - Visualizador A*")

clock = pygame.time.Clock()

# Fuente robótica
font_default = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 32)
font_title = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 52)
font_little = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 20)

menu = MenuScreen(screen)
game = GameScreen(screen)

current_screen = menu
running = True

while running:
    dt = clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        next_screen, elements = current_screen.handle_events(event)

        if next_screen:
            current_screen = game if next_screen == "game" else menu
            current_screen.dim = elements[0] # Al cambiar pantalla pasamos las dimensiones

    current_screen.show()

    pygame.display.flip()

pygame.quit()
sys.exit()