import pygame
import numpy as np

from ui.popup import Popup
from ui.colors import Colors
from ui.button import Button
from ui.ui_actions import UIActions

from core.astar import Astar
from core.event_dispatcher import EventDispatcher

WIDTH = 1280
HEIGHT = 720

info_button = pygame.Rect((WIDTH-80), 10, 50, 50)
info_rect = pygame.Rect(0, 0, 500, 300)
info_rect.center = (WIDTH//2, HEIGHT//2)

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
        self.restart_icon = pygame.image.load("./assets/icons/reload_icon.png").convert_alpha()
        self.restart_icon = pygame.transform.smoothscale(self.restart_icon, (46, 46))

        self.mapa_size = 620
        self.grid_origin_x = 40
        self.grid_origin_y = 80

        # BOTONES

        self.back_button = Button(
            rect=(20, 20, 80, 42),
            base_color=Colors.ORANGE_LIGHT,
            hover_color=Colors.ORANGE,
            text="<=",
            font=self.font_default
        )

        self.info_button = Button(
            rect=(WIDTH-80, 10, 50, 50),
            base_color=Colors.BLUE,
            hover_color=Colors.BLUE_DARK,
            text="?",
            font=self.font_default,
            border_radius=25
        )

        self.init_button = Button(
            rect=(WIDTH - 500, 160, 160, 160),
            base_color=Colors.BLUE,
            hover_color=Colors.BLUE_DARK,
            border_radius=10,
            border=4
        )

        self.goal_button = Button(
            rect=(WIDTH - 300, 160, 160, 160),
            base_color=Colors.GREEN,
            hover_color=Colors.GREEN_DARK,
            border_radius=10,
            border=4
        )

        self.obstacle_button = Button(
            rect=(WIDTH - 400, 360, 160, 160),
            base_color=Colors.GRAY,
            hover_color=Colors.GRAY_DARK,
            border_radius=10,
            border=4
        )

        self.restart_button = Button(
            rect=(WIDTH - 100, 630, 60, 60),
            base_color=Colors.RED,
            hover_color=Colors.RED_DARK,
            icon=self.restart_icon,
            border_radius=10
        )

        self.execute_button = Button(
            rect=(WIDTH - 540, 630, 420, 60),
            base_color=Colors.BLUE,
            hover_color=Colors.BLUE_DARK,
            text="Ejecutar",
            font=self.font_default,
            border_radius=10
        )

        self.buttons = [
            self.back_button,
            self.info_button,
            self.init_button,
            self.goal_button,
            self.obstacle_button,
            self.restart_button,
            self.execute_button
        ]

        # COLORES DE CELDAS
        self.cell_colors = {
            0: Colors.GRAY_LIGHT,   # vacío
            1: Colors.BLUE,         # inicio
            2: Colors.GREEN,        # meta
            3: Colors.YELLOW,       # camino
            -1: Colors.GRAY         # obstáculo
        }

        self.dispatcher = EventDispatcher()
        self.ui_actions = UIActions(self)

        self.dispatcher.register(self.info_button, self.ui_actions.on_info_click)
        self.dispatcher.register(self.execute_button, self.ui_actions.on_execute_click)
        self.dispatcher.register(self.back_button, lambda: ("menu", None))
        self.dispatcher.register(self.restart_button, self.ui_actions.on_restart_click)
        self.dispatcher.register(self.init_button, self.ui_actions.on_select_init)
        self.dispatcher.register(self.goal_button, self.ui_actions.on_select_goal)
        self.dispatcher.register(self.obstacle_button, self.ui_actions.on_select_obstacle)

        # ANIMACION
        self.lista_animacion = []
        self.animando = False
        self.timer_animacion = 0
        self.velocidad_animacion = 50 # ms por cada paso

    def set_dim(self, dim):
        self.dim = dim
        self.matriz_astar = np.zeros((self.dim, self.dim), dtype=int)
    
    def show(self):
        
        self.screen.fill(Colors.GRAY_LIGHT)
        dim_text = self.font_default.render(f"Dimensiones: {self.dim}x{self.dim}", True, (0,0,0))

        self.dibujar_mapa()

        self.screen.blit(dim_text, (120, 30))

        mouse_pos = pygame.mouse.get_pos()
        
        # Dibujar los botones
        for button in self.buttons:
            button.draw(self.screen, mouse_pos)

        if self.popup.info_active:
            self.popup.info_pop()

        if self.popup.error_active:
            self.popup.error_pop("No has dibujado correctamente el mapa")

        self.animar_busqueda()

        self.manejar_mouse_mantenido()



    def handle_events(self, event):
        if self.popup.info_active or self.popup.error_active:
            self.popup.handle_events(event)
            return None, None
        
        result = self.dispatcher.handle_event(event)
        if result:
            return result
        
        if event.type == pygame.MOUSEBUTTONDOWN:

            celda = self.get_celda(event.pos)

            if celda:
                row, col = celda

                if event.button == 1:
                    if self.selected_button == "init":
                        if self.pos_init:
                            prev_row, prev_col = self.pos_init
                            self.matriz_astar[prev_row][prev_col] = 0
                        self.pos_init = (row, col)
                        self.matriz_astar[row][col] = 1

                    elif self.selected_button == "goal":
                        if self.pos_goal:
                            prev_row, prev_col = self.pos_goal
                            self.matriz_astar[prev_row][prev_col] = 0

                        self.pos_goal = (row, col)
                        self.matriz_astar[row][col] = 2
                    elif self.selected_button == "obstacle":
                        self.matriz_astar[row][col] = -1

                elif event.button == 3:
                    if self.matriz_astar[row][col] == 3:
                        return None, None
                    
                    self.matriz_astar[row][col] = 0

                    # Limpiar posiciones guardadas si se borran
                    if self.pos_init == (row, col):
                        self.pos_init = None

                    if self.pos_goal == (row, col):
                        self.pos_goal = None

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

                celda = self.matriz_astar[row][col]

                # Color base según matriz
                color = self.cell_colors.get(celda, Colors.GRAY_LIGHT)

                if celda == 0 and rect.collidepoint(mouse_pos):
                    color = Colors.GRAY_DARK    

                pygame.draw.rect(self.screen, color, rect)  # resaltar celda
                pygame.draw.rect(self.screen, Colors.BLACK, rect, 1)  # borde


    def dibujar_busqueda(self, lista_astar):

            # Popeamos los últimos elementos de la lista abierta y cerrada para mostrar el proceso de búsqueda
            lista_astar.pop(0)
            lista_astar.pop(-1)
            for x, y in lista_astar:
                self.matriz_astar[x][y] = 3  # Marcar el camino encontrado (puedes usar otro valor para diferenciarlo)



    def get_celda(self, pos):
        x, y = pos
        tam = self.get_tam_celda()

        # verificar si está dentro del grid
        if not (
            self.grid_origin_x <= x < self.grid_origin_x + self.mapa_size and
            self.grid_origin_y <= y < self.grid_origin_y + self.mapa_size
        ):
            return None

        col = (x - self.grid_origin_x) // tam
        row = (y - self.grid_origin_y) // tam

        if 0 <= row < self.dim and 0 <= col < self.dim:
            return int(row), int(col)

        return None
    
    def get_tam_celda(self):
        return self.mapa_size // self.dim
    
    def animar_busqueda(self):
        if self.animando and self.lista_animacion:

            ahora = pygame.time.get_ticks()

            if ahora - self.timer_animacion > self.velocidad_animacion:

                x, y = self.lista_animacion.pop(0)
                self.matriz_astar[x][y] = 3

                self.timer_animacion = ahora

        elif not self.lista_animacion:
            self.animando = False

    def manejar_mouse_mantenido(self):
        botones = pygame.mouse.get_pressed()

        if botones[0]:  # Si se mantiene presionado el botón izquierdo del mouse
            celda = self.get_celda(pygame.mouse.get_pos())

            if celda:
                row, col = celda

                if self.selected_button == "obstacle":
                    self.matriz_astar[row][col] = -1
        
        if botones[2]:
            celda = self.get_celda(pygame.mouse.get_pos())

            if celda:
                row, col = celda

                if self.matriz_astar[row][col] not in (1, 2):  
                    self.matriz_astar[row][col] = 0