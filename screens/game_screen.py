import pygame

from ui.popup import Popup
from ui.colors import Colors
from core.astar import AStar

WIDTH = 1280
HEIGHT = 720

info_button = pygame.Rect((WIDTH-80), 10, 50, 50)
info_rect = pygame.Rect(0, 0, 500, 300)
info_rect.center = (WIDTH//2, HEIGHT//2)
close_button = pygame.Rect(info_rect.right - 40, info_rect.y + 10, 30, 30)

execute_button = pygame.Rect((WIDTH-540), 630, 480, 60)

selected_button = None

matriz_astar = []

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


        # TODO los 3 botones para pintar el juego

        pygame.draw.rect(self.screen, Colors.BLUE, pygame.Rect(WIDTH - 500, 160, 160, 160), border_radius=10)
        pygame.draw.rect(self.screen, Colors.GREEN, pygame.Rect(WIDTH - 300, 160, 160, 160), border_radius=10)
        pygame.draw.rect(self.screen, Colors.GRAY, pygame.Rect(WIDTH - 400, 360, 160, 160), border_radius=10)

        # TODO boton para ejecutar el algoritmo

        execute_button_color = Colors.BLUE_DARK if execute_button.collidepoint(mouse_pos) else Colors.BLUE
        pygame.draw.rect(self.screen, execute_button_color, execute_button, border_radius=10)
        execute_text = self.font_default.render("Ejecutar", True, Colors.WHITE)
        self.screen.blit(execute_text, (execute_button.centerx - 110, execute_button.centery - 15))

        if self.popup.active:
            self.popup.pop()

    def handle_events(self, event):
        if self.popup.active:
            self.popup.handle_events(event)
            return None, None
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if info_button.collidepoint(event.pos):
                self.popup.active = True

            if execute_button.collidepoint(event.pos):
                # TODO ejecutar el algoritmo A* y mostrar el resultado
                astar = AStar(self.dim, matriz_astar)
                astar.ejecutar()
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