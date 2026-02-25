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
        try:

            self.screen.matriz_astar[self.screen.matriz_astar == 3] = 0

            if self.screen.pos_init and self.screen.pos_goal:
                astar = Astar(self.screen.dim, self.screen.matriz_astar)
                lista_astar = astar.ejecutar()
                lista_astar.pop(0)
                lista_astar.pop(-1)

                self.screen.lista_animacion = lista_astar.copy()
                self.screen.animando = True
                self.screen.timer_animacion = pygame.time.get_ticks()
                
        except Exception as e:
            self.screen.popup.error_active = True


    def on_restart_click(self):
        self.screen.matriz_astar = np.zeros((self.screen.dim, self.screen.dim), dtype=int)
        self.screen.pos_init = None
        self.screen.pos_goal = None

    def on_select_init(self):
        self.screen.selected_button = "init"

    def on_select_goal(self):
        self.screen.selected_button = "goal"

    def on_select_obstacle(self):
        self.screen.selected_button = "obstacle"

        