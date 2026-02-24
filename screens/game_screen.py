import pygame
import numpy as np

from ui.popup import Popup
from ui.colors import Colors
from core.astar import Astar

WIDTH = 1280
HEIGHT = 720

info_button = pygame.Rect((WIDTH-80), 10, 50, 50)
info_rect = pygame.Rect(0, 0, 500, 300)
info_rect.center = (WIDTH//2, HEIGHT//2)
close_button = pygame.Rect(info_rect.right - 40, info_rect.y + 10, 30, 30)

execute_button = pygame.Rect((WIDTH-540), 630, 480, 60)
back_button = pygame.Rect(20, 630, 160, 60)
init_button = pygame.Rect(WIDTH - 500, 160, 160, 160)
goal_button = pygame.Rect(WIDTH - 300, 160, 160, 160)
obstacle_button = pygame.Rect(WIDTH - 400, 360, 160, 160)

class GameScreen:

    def __init__(self, screen, dim = 0):
        self.screen = screen
        self.dim = dim
        self.font_little = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 20)
        self.font_default = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 32)
        self.font_title = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 52)
        self.popup = Popup(screen)
        self.selected_button = ""
        self.matriz_astar = np.zeros((self.dim, self.dim), dtype=int)
        self.pos_init = None   # Guarda (row, col) de inicio
        self.pos_goal = None   # Guarda (row, col) de meta
        self.terminado = False

    def set_dim(self, dim):
        self.dim = dim
        self.matriz_astar = np.zeros((self.dim, self.dim), dtype=int)
    
    def show(self):
        
        self.screen.fill(Colors.GRAY_LIGHT)
        dim_text = self.font_default.render(f"Dimensiones: {self.dim}x{self.dim}", True, (0,0,0))




        self.dibujar_mapa()

        self.screen.blit(dim_text, (120, 30))

        mouse_pos = pygame.mouse.get_pos()

        # TODO crear botón para regresar al menú principal
        
        back_button_color = Colors.ORANGE if back_button.collidepoint(mouse_pos) else Colors.ORANGE_LIGHT
        pygame.draw.rect(self.screen, back_button_color, back_button, border_radius=10)
        back_text = self.font_default.render("V", True, Colors.WHITE)
        self.screen.blit(back_text, (back_button.centerx - 80, back_button.centery - 15))

        # Boton de información
        button_color = Colors.BLUE_DARK if info_button.collidepoint(mouse_pos) else Colors.BLUE
        pygame.draw.rect(self.screen, button_color, info_button, border_radius=25)
        info_text_button = self.font_default.render("?", True, Colors.WHITE)
        self.screen.blit(info_text_button, ((WIDTH-69), 22))

        init_button_color = Colors.BLUE_DARK if init_button.collidepoint(mouse_pos) else Colors.BLUE        
        pygame.draw.rect(self.screen, init_button_color, init_button, border_radius=10)

        goal_button_color = Colors.GREEN_DARK if goal_button.collidepoint(mouse_pos) else Colors.GREEN
        pygame.draw.rect(self.screen, goal_button_color, goal_button, border_radius=10)

        obstacle_button_color = Colors.GRAY_DARK if obstacle_button.collidepoint(mouse_pos) else Colors.GRAY
        pygame.draw.rect(self.screen, obstacle_button_color, obstacle_button, border_radius=10)

        # TODO boton para reiniciar todo el proceso

        restart_button = pygame.Rect(WIDTH - 100, 10, 80, 40)
        restart_button_color = Colors.RED_DARK if restart_button.collidepoint(mouse_pos) else Colors.RED
        pygame.draw.rect(self.screen, restart_button_color, restart_button, border_radius=10)
        restart_text = self.font_default.render("R", True, Colors.WHITE) # TODO MUST BE ICON
        self.screen.blit(restart_text, (restart_button.centerx - 35, restart_button.centery - 15))

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
                # Las matrices con 3 las pasamos a 0 para no interferir con el proceso de búsqueda
                self.matriz_astar[self.matriz_astar == 3] = 0

                astar = Astar(self.dim, self.matriz_astar)
                lista_astar = astar.ejecutar()
                self.dibujar_busqueda(lista_astar)

            if back_button.collidepoint(event.pos):
                return "menu", None

            if init_button.collidepoint(event.pos):
                self.selected_button = "init"

            if goal_button.collidepoint(event.pos):
                self.selected_button = "goal"

            if obstacle_button.collidepoint(event.pos):
                self.selected_button = "obstacle"

            for row in range(self.dim):
                for col in range(self.dim):
                    mapa = 620
                    tam_celdas = mapa // self.dim

                    coord_x = 40 + col * tam_celdas
                    coord_y = 80 + row * tam_celdas

                    rect = pygame.Rect(coord_x, coord_y, tam_celdas, tam_celdas)

                    if rect.collidepoint(event.pos):
                        if self.selected_button == "init":
                            pygame.draw.rect(self.screen, Colors.BLUE, rect)  # resaltar celda de inicio

                            if self.pos_init is not None:
                                # Si ya hay una posición de inicio, la limpiamos
                                prev_row, prev_col = self.pos_init
                                self.matriz_astar[prev_row][prev_col] = 0  # Limpiar celda anterior

                            self.pos_init = (row, col)
                            self.matriz_astar[row][col] = 1
                        elif self.selected_button == "goal":
                            pygame.draw.rect(self.screen, Colors.GREEN, rect)  # resaltar celda de meta

                            if self.pos_goal is not None:
                                # Si ya hay una posición de meta, la limpiamos
                                prev_row, prev_col = self.pos_goal
                                self.matriz_astar[prev_row][prev_col] = 0  # Limpiar celda anterior
                            
                            self.pos_goal = (row, col)
                            self.matriz_astar[row][col] = 2
                        elif self.selected_button == "obstacle":
                            pygame.draw.rect(self.screen, Colors.GRAY, rect)  # resaltar celda de obstáculo
                            self.matriz_astar[row][col] = -1
        return None, None

    

    def dibujar_mapa(self):
        mapa = 620
        tam_celdas = mapa // self.dim

        coord_x = 40
        coord_y = 80

        mouse_pos = pygame.mouse.get_pos()

        for row in range(self.dim):
            for col in range(self.dim):

                rect = pygame.Rect(
                    coord_x + col * tam_celdas,
                    coord_y + row * tam_celdas,
                    tam_celdas,
                    tam_celdas                
                )

                if rect.collidepoint(mouse_pos):
                    color = Colors.GRAY
                else:
                    color = Colors.GRAY_LIGHT

                # Colores según matriz
                if self.matriz_astar[row][col] == 1:  # inicio
                    color = Colors.BLUE
                elif self.matriz_astar[row][col] == 2:  # meta
                    color = Colors.GREEN
                elif self.matriz_astar[row][col] == 3:  # camino encontrado
                    color = Colors.YELLOW
                elif self.matriz_astar[row][col] == -1:  # obstáculo
                    color = Colors.GRAY
                elif rect.collidepoint(mouse_pos):  # hover
                    color = Colors.GRAY_DARK
                else:
                    color = Colors.GRAY_LIGHT

                pygame.draw.rect(self.screen, color, rect)  # resaltar celda
                pygame.draw.rect(self.screen, Colors.BLACK, rect, 1)  # borde

    def dibujar_busqueda(self, lista_astar):
        # Popeamos los últimos elementos de la lista abierta y cerrada para mostrar el proceso de búsqueda
        lista_astar.pop(0)
        lista_astar.pop(-1)
        self.terminado = True # Fin del proceso de búsqueda
        print("Lista A*:", lista_astar)
        for x, y in lista_astar:
            self.matriz_astar[x][y] = 3  # Marcar el camino encontrado (puedes usar otro valor para diferenciarlo)
            print(x, y)
