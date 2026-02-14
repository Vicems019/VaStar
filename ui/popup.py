import pygame

from ui.colors import Colors
WIDTH = 1280
HEIGHT = 720

class Popup:

    def __init__(self, screen):
        self.screen = screen
        self.active = False
        self.font_little = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 20)
        self.font_default = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 32)
        self.font_title = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 52)

        self.rect = pygame.Rect((WIDTH-400)//2, (HEIGHT-600)//2, 580, 500)

        self.close_button = pygame.Rect(
            self.rect.right - 35,
            self.rect.y + 10,
            30,
            30
        )

        self.paleta_items = [
            (Colors.GREEN_LIGHT, "Inicio"),
            (Colors.BLUE_LIGHT, "Final"),
            (Colors.RED, "Recorrido"),
            (Colors.YELLOW_LIGHT, "Camino más rápido"),
            (Colors.GRAY, "Obstáculo")
        ]

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button.collidepoint(event.pos):
                self.active = False

    def pop(self):

        mouse_pos = pygame.mouse.get_pos()
        close_color = Colors.RED_DARK if self.close_button.collidepoint(mouse_pos) else Colors.RED

        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(150)
        overlay.fill(Colors.BLACK)
        self.screen.blit(overlay, (0, 0))

        pygame.draw.rect(self.screen, Colors.WHITE, self.rect)
        pygame.draw.rect(self.screen, Colors.BLACK, self.rect, 2)
        pygame.draw.rect(self.screen, close_color, self.close_button)


        # Dibujar paleta de colores + info

        for i, (color, texto) in enumerate(self.paleta_items):
            rect_cuadrado = pygame.Rect(
                self.rect.left + 50,
                self.rect.top + 90 + i*80,
                35,
                35
            )

            # Cuadrado Paleta
            pygame.draw.rect(self.screen, color, rect_cuadrado)
            pygame.draw.rect(self.screen, Colors.BLACK, rect_cuadrado, 2)

            # Info Paleta
            text_paleta = self.font_little.render(texto, True, Colors.BLACK)
            rect_paleta = text_paleta.get_rect(
                midleft=(rect_cuadrado.right+40, rect_cuadrado.centery)
            )

            self.screen.blit(text_paleta, rect_paleta)

        info_title = self.font_default.render("Información", True, Colors.BLACK)
        self.screen.blit(info_title, (self.rect.left+20, self.rect.top+20))

        x_text = self.font_little.render("X", True, Colors.WHITE)
        x_rect = x_text.get_rect(center=self.close_button.center)
        self.screen.blit(x_text, x_rect)