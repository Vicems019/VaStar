import pygame
import sys

pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VaStar - Visualizador A*")

clock = pygame.time.Clock()

# Fuente robótica
font_default = pygame.font.Font("PressStart2P-Regular.ttf", 32)
font_title = pygame.font.Font("PressStart2P-Regular.ttf", 52)

running = True

# --- Estado ---
size_text = ""
size_input = pygame.Rect((WIDTH-260)//2, HEIGHT//2, 140, 40)
size_button = pygame.Rect((WIDTH+60)//2, HEIGHT//2, 100, 40)
active = False


def set_dimensiones(value):
    mensaje = (
        "Introduce un número"
        if value == ""
        else f"Dimensiones del mapa {value}x{value}"
    )

    if len(value) == 0:
        x = 320
    elif len(value) <= 2:
        x = 240
    else:
        x = 190

    message_surface = font_default.render(mensaje, True, (0, 0, 0))

    screen.blit(message_surface, (x, 280))
        
        

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
                try:
                    if int(size_text) > 0:
                        #TODO new panel with the map
                        pass

                except:
                    raise TypeError("Can't parse into int")
                

        # Detectar escritura
        if event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_BACKSPACE:
                size_text = size_text[:-1]
            elif event.unicode.isdigit():
                if len(size_text) < 4:
                    size_text += event.unicode

    screen.fill((200, 200, 200))

    # PANEL PRINCIPAL
    text_main = font_title.render("Bienvenido a VaStar*", True, (0, 0, 0))
    screen.blit(text_main, (130, 100))

    # Cambiar color si está activo
    input_color = (120, 120, 120) if active else (90, 90, 90)

    # Campo input
    pygame.draw.rect(screen, input_color, size_input, border_radius=10)
    surface_text = font_default.render(size_text, True, (0, 180, 180))
    screen.blit(surface_text, (size_input.x + 10, size_input.y + 5))

    # Botón
    pygame.draw.rect(screen, (0, 120, 200), size_button, border_radius=5)
    button_text = font_default.render("OK", True, (255, 255, 255))
    screen.blit(button_text, (size_button.x + 20, size_button.y + 5))

    # Texto dinámico
    message = set_dimensiones(size_text)
    message_surface = font_default.render(message, True, (0, 0, 0))
    screen.blit(message_surface, (320, 280))

    pygame.display.flip()

pygame.quit()
sys.exit()