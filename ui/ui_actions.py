import pygame

from core.astar import Astar

from ui.popup import Popup

import numpy as np

class UIActions:
    def __init__(self, screen):
        self.screen = screen

        self.mapa_size = 620
        self.grid_origin_x = 40
        self.grid_origin_y = 80

    def on_info_click(self):
        self.screen.popup.info_active = True

    def on_execute_click(self):
        self.screen.matriz_astar[self.screen.matriz_astar == 3] = 0
        self.screen.matriz_astar[self.screen.matriz_astar == 4] = 0
        self.screen.matriz_astar[self.screen.matriz_astar == 5] = 0  # limpiar exploradas también

        if self.screen.pos_init and self.screen.pos_goal:
            astar = Astar(self.screen.dim, self.screen.matriz_astar)
            # Guardamos el generador, no ejecutamos todo de golpe
            self.screen.generador_astar = astar.ejecutar()
            self.screen.animando = True
            self.screen.timer_animacion = pygame.time.get_ticks()

    def on_restart_click(self):
        # Limpiamos la matriz y posiciones
        self.screen.matriz_astar = np.zeros((self.screen.dim, self.screen.dim), dtype=int)
        self.screen.pos_init = None
        self.screen.pos_goal = None
        self.estado = None

        # Detenemos la animación
        self.screen.animando = False
        self.screen.generador_astar = None

    def on_select_init(self):
        self.screen.selected_button = "init"

    def on_select_goal(self):
        self.screen.selected_button = "goal"

    def on_select_obstacle(self):
        self.screen.selected_button = "obstacle"

    def on_cell_pressed(self, event):
        botones = pygame.mouse.get_pressed()

        if botones[0]:  # Si se mantiene presionado el botón izquierdo del mouse
            celda = self.get_celda(pygame.mouse.get_pos())

            if celda:
                row, col = celda

                if self.screen.selected_button == "obstacle":
                    self.screen.matriz_astar[row][col] = -1
        
        if botones[2]:
            celda = self.get_celda(pygame.mouse.get_pos())

            if celda:
                row, col = celda

                # Eliminamos elementos de la casilla seleccionada
                if self.screen.matriz_astar[row][col] not in (1, 2):  
                    self.screen.matriz_astar[row][col] = 0

    def on_cell_actions(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return None, None

        celda = self.get_celda(event.pos)

        if not celda:
            return None, None

        row, col = celda

        # CLICK IZQUIERDO
        if event.button == 1:

            if self.screen.selected_button == "init":

                if self.screen.pos_init:
                    prev_row, prev_col = self.screen.pos_init
                    self.screen.matriz_astar[prev_row][prev_col] = 0

                self.screen.pos_init = (row, col)
                self.screen.matriz_astar[row][col] = 1

            elif self.screen.selected_button == "goal":

                if self.screen.pos_goal:
                    prev_row, prev_col = self.screen.pos_goal
                    self.screen.matriz_astar[prev_row][prev_col] = 0

                self.screen.pos_goal = (row, col)
                self.screen.matriz_astar[row][col] = 2

            elif self.screen.selected_button == "obstacle":

                self.screen.matriz_astar[row][col] = -1

        # CLICK DERECHO
        elif event.button == 3:

            if self.screen.matriz_astar[row][col] == 3:
                return None, None

            self.screen.matriz_astar[row][col] = 0

            if self.screen.pos_init == (row, col):
                self.screen.pos_init = None

            if self.screen.pos_goal == (row, col):
                self.screen.pos_goal = None

        return None, None
    

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

        if 0 <= row < self.screen.dim and 0 <= col < self.screen.dim:
            return int(row), int(col)

        return None
    
    def get_tam_celda(self):
        return self.screen.mapa_size // self.screen.dim
    