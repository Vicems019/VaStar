import pygame

from core.astar import Astar

from ui.popup import Popup

import numpy as np

class UIActions:
    def __init__(self, screen):
        self.screen = screen

    def on_info_click(self):
        self.screen.popup.info_active = True

    def on_execute_click(self):
        self.screen.matriz_astar[self.screen.matriz_astar == 3] = 0
        self.screen.matriz_astar[self.screen.matriz_astar == 4] = 0  # limpiar exploradas también

        if self.screen.pos_init and self.screen.pos_goal:
            astar = Astar(self.screen.dim, self.screen.matriz_astar)
            # Guardamos el generador, no ejecutamos todo de golpe
            self.screen.generador_astar = astar.ejecutar()
            self.screen.animando = True
            self.screen.timer_animacion = pygame.time.get_ticks()

    # TODO EL BOTON RESTART TIENE QUE PARAR LA EJECUCIÓN DEL CÓDIGO
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

        