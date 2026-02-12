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

# --- Estado ---
size_text = ""
size_input = pygame.Rect(50, 50, 140, 40)
size_button = pygame.Rect(200, 50, 100, 40)
active = False


def get_message(value):
    if value == "":
        return "Introduce un número"
    try:
        num = int(value)
        if num > 10:
            return "Número grande"
        else:
            return "Número pequeño"
    except:
        return "Solo números"

while running:
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Detectar click del mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            if size_input.collidepoint(event.pos):
                active = True
            else:
                active = False

            if size_button.collidepoint(event.pos):
                print("Botón pulsado. Valor:", size_text)

        # Detectar escritura
        if event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_BACKSPACE:
                size_text = size_text[:-1]
            elif event.unicode.isdigit():
                size_text += event.unicode

    screen.fill((200, 200, 200))

    # PANEL PRINCIPAL
    text_main = font.render("Introduce un tamaño", True, (0, 255, 180))
    screen.blit(text_main, (20, 20))

    # Cambiar color si está activo
    input_color = (120, 120, 120) if active else (90, 90, 90)

    # Campo input
    pygame.draw.rect(screen, input_color, size_input, border_radius=10)
    surface_text = font.render(size_text, True, (0, 255, 180))
    screen.blit(surface_text, (size_input.x + 10, size_input.y + 5))

    # Botón
    pygame.draw.rect(screen, (0, 120, 200), size_button, border_radius=5)
    button_text = font.render("OK", True, (255, 255, 255))
    screen.blit(button_text, (size_button.x + 30, size_button.y + 5))

    # Texto dinámico
    message = get_message(size_text)
    message_surface = font.render(message, True, (0, 0, 0))
    screen.blit(message_surface, (50, 110))

    pygame.display.flip()

pygame.quit()
sys.exit()