import pygame

WIDTH = 1280
HEIGHT = 720

class Popup:

    def __init__(self, screen):
        self.screen = screen
        self.active = False
        self.font_little = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 20)
        self.font_default = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 32)
        self.font_title = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 52)

        self.rect = pygame.Rect((WIDTH-400)//2, (HEIGHT-600)//2, 400, 600)

        self.close_button = pygame.Rect(
            self.rect.right - 35,
            self.rect.y + 10,
            30,
            30
        )

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button.collidepoint(event.pos):
                self.active = False

    def pop(self):

        mouse_pos = pygame.mouse.get_pos()
        close_color = (170, 30, 30) if self.close_button.collidepoint(mouse_pos) else (200, 50, 50)

        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        pygame.draw.rect(self.screen, (240, 240, 240), self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        pygame.draw.rect(self.screen, close_color, self.close_button)


        # Dibujar paleta de colores + info
        # TODO DIBUJAR PALETA Y LOS TEXTOS DE INFORMACIÓN

        info_title = self.font_little.render("Información", True, (0,0,0))
        self.screen.blit(info_title, (self.rect.left+20, self.rect.top+10))

        x_text = self.font_little.render("X", True, (255, 255, 255))
        x_rect = x_text.get_rect(center=self.close_button.center)
        self.screen.blit(x_text, x_rect)