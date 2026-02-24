from core.astar import Astar
import numpy as np

class UIActions:
    def __init__(self, screen):
        self.screen = screen

    def on_info_click(self):
        self.screen.popup.active = True


    def on_execute_click(self):
        self.screen.matriz_astar[self.screen.matriz_astar == 3] = 0

        if self.screen.pos_init and self.screen.pos_goal:
            astar = Astar(self.screen.dim, self.screen.matriz_astar)
            lista_astar = astar.ejecutar()
            self.screen.dibujar_busqueda(lista_astar)


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