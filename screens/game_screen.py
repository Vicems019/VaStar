import pygame

from ui.popup import Popup
from ui.colors import Colors

WIDTH = 1280
HEIGHT = 720

info_button = pygame.Rect((WIDTH-80), 10, 50, 50)
info_rect = pygame.Rect(0, 0, 500, 300)
info_rect.center = (WIDTH//2, HEIGHT//2)
close_button = pygame.Rect(info_rect.right - 40, info_rect.y + 10, 30, 30)

class GameScreen:


    def __init__(self, screen, dim = 0):
        self.screen = screen
        self.dim = dim
        self.font_little = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 20)
        self.font_default = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 32)
        self.font_title = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 52)
        self.popup = Popup(screen)

    
    def show(self):
        
        self.screen.fill(Colors.GRAY_LIGHT)
        dim_text = self.font_default.render(f"Dimensiones: {self.dim}x{self.dim}", True, (0,0,0))

        self.dibujar_mapa()

        self.screen.blit(dim_text, (20, 30))

        mouse_pos = pygame.mouse.get_pos()

        # Boton de información
        button_color = Colors.BLUE_DARK if info_button.collidepoint(mouse_pos) else Colors.BLUE
        pygame.draw.rect(self.screen, button_color, info_button, border_radius=25)
        info_text_button = self.font_default.render("?", True, Colors.WHITE)
        self.screen.blit(info_text_button, ((WIDTH-69), 22))


        # TODO los 4 botones para pintar el juego

        for i in range(4):
            x = WIDTH - 80
            y = 80 + i*60
            pygame.draw.rect(self.screen, Colors.YELLOW, pygame.Rect(x, y, 50, 50), border_radius=10)
            

        # TODO boton para ejecutar el algoritmo

        if self.popup.active:
            self.popup.pop()

    def handle_events(self, event):
        if self.popup.active:
            self.popup.handle_events(event)
            return None, None
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if info_button.collidepoint(event.pos):
                self.popup.active = True
        return None, None

    

    def dibujar_mapa(self):
        mapa = 620
        tam_celdas = mapa // self.dim

        coord_x = 40
        coord_y = 80

        for row in range(self.dim):
            for col in range(self.dim):

                rect = pygame.Rect(
                    coord_x + col * tam_celdas,
                    coord_y + row * tam_celdas,
                    tam_celdas,
                    tam_celdas                
                )

                pygame.draw.rect(self.screen, Colors.BLACK, rect, 1)  # borde