from core.node import Node
import numpy as np

class Astar:
    def __init__(self, dim, matriz):
        self.dim = dim
        self.matriz = matriz

    def ejecutar(self):
        print("MATRIZ OBTENIDA:\n\n", self.matriz)

        # Declaramos el nodo inicial y el nodo objetivo
        pos_init_x, pos_init_y = np.where(self.matriz == 1)
        pos_end_x, pos_end_y = np.where(self.matriz == 2)

        nodo_inicial = Node(None, (pos_init_x[0], pos_init_y[0]))
        nodo_inicial.g = nodo_inicial.h = nodo_inicial.f = 0


        nodo_final = Node(None, (pos_end_x[0], pos_end_y[0]))
        nodo_final.g = nodo_final.h = nodo_final.f = 0

        # Creamos las listas abierta y cerrada
        lista_abierta = []
        lista_cerrada = []

        # Añadimos el nodo inicial a la lista abierta
        lista_abierta.append(nodo_inicial)

        # Iteramos hasta encontrar el nodo objetivo
        while len(lista_abierta) > 0:

            # Nodo actual
            nodo_actual = lista_abierta[0]
            indice_actual = 0

            # Recorremos la lista abierta para encontrar el nodo con el menor valor de f
            for indice, nodo in enumerate(lista_abierta):
                if nodo.f < nodo_actual.f:
                    nodo_actual = nodo
                    indice_actual = indice

            # Eliminamos el nodo actual de la lista abierta y lo añadimos a la lista cerrada
            lista_abierta.pop(indice_actual)
            lista_cerrada.append(nodo_actual)

            # Si el nodo actual es el nodo objetivo, hemos encontrado la solución
            if nodo_actual == nodo_final:
                camino = []
                nodo = nodo_actual
                while nodo is not None:
                    print(nodo)
                    print(type(nodo))
                    camino.append(nodo.position)
                    nodo = nodo.parent
                return camino[::-1]  # Devolvemos el camino desde el nodo inicial al nodo objetivo
            
            # Generamos los hijos del nodo actual
            hijos = []
            for nueva_posicion in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Movimientos posibles (4 direcciones + diagonales)
                nodo_posicion = (nodo_actual.position[0] + nueva_posicion[0], nodo_actual.position[1] + nueva_posicion[1])

                # Aseguramos que el nodo esté dentro de los límites del mapa
                if nodo_posicion[0] < 0 or nodo_posicion[0] >= self.dim or nodo_posicion[1] < 0 or nodo_posicion[1] >= self.dim:
                    continue

                # Aseguramos que el nodo no sea un obstáculo
                if self.matriz[nodo_posicion[0]][nodo_posicion[1]] == -1:
                    continue

                nuevo_nodo = Node(nodo_actual, nodo_posicion)
                hijos.append(nuevo_nodo)

            # Recorremos los hijos del nodo actual
            for hijo in hijos:
                # Si el hijo ya está en la lista cerrada, lo ignoramos
                if hijo in lista_cerrada:
                    continue

                # Calculamos los valores de g, h y f para el hijo
                hijo.g = nodo_actual.g + 1
                hijo.h = ((hijo.position[0] - nodo_final.position[0]) ** 2) + ((hijo.position[1] - nodo_final.position[1]) ** 2) # Heurística de Manhattan
                hijo.f = hijo.g + hijo.h

                # Si el hijo ya está en la lista abierta con un valor de g menor, lo ignoramos
                for nodo_abierto in lista_abierta:
                    if hijo == nodo_abierto and hijo.g > nodo_abierto.g:
                        continue

                # Añadimos el hijo a la lista abierta
                lista_abierta.append(hijo)