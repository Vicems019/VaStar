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
current_screen = "menu"
dim = 0

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
        

def dibujar_mapa(dim):
    mapa = 600
    tam_celdas = mapa // dim

    coord_x = 60
    coord_y = 100

    for row in range(dim):
        for col in range(dim):

            rect = pygame.Rect(
                coord_x + col * tam_celdas,
                coord_y + row * tam_celdas,
                tam_celdas,
                tam_celdas
            )

            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # borde

while running:
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Eventos del menu
        if current_screen == "menu":

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if size_input.collidepoint(event.pos):
                    active = True
                else:
                    active = False

                if size_button.collidepoint(event.pos):
                    try:
                        if int(size_text) > 0:
                            current_screen = "game"
                            dim = int(size_text)
                    except:
                        pass

            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    size_text = size_text[:-1]
                elif event.unicode.isdigit():
                    if len(size_text) < 4:
                        size_text += event.unicode
        elif current_screen == "game":
            pass

    screen.fill((200, 200, 200))

    # Diseño del menu
    if current_screen == "menu":

        text_main = font_title.render("Bienvenido a VaStar*", True, (0, 0, 0))
        screen.blit(text_main, (130, 100))

        input_color = (120, 120, 120) if active else (90, 90, 90)

        pygame.draw.rect(screen, input_color, size_input, border_radius=10)
        surface_text = font_default.render(size_text, True, (0, 180, 180))
        screen.blit(surface_text, (size_input.x + 10, size_input.y + 5))

        pygame.draw.rect(screen, (0, 120, 200), size_button, border_radius=5)
        button_text = font_default.render("OK", True, (255, 255, 255))
        screen.blit(button_text, (size_button.x + 20, size_button.y + 5))

        set_dimensiones(size_text)

    # Diseño del mapa
    elif current_screen == "game":

        dim_text = font_default.render(f"Dimensiones: {dim}x{dim}", True, (0,0,0))

        dibujar_mapa(dim)

        # TODO Boton de ayuda para explicar lo que hace cada pintura

        screen.blit(dim_text, (40, 40))

    pygame.display.flip() # Actualizar cambio de pantallas

pygame.quit()
sys.exit()