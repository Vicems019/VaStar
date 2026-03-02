from core.node import Node
import numpy as np

class Astar:
    def __init__(self, dim, matriz):
        self.dim = dim
        self.matriz = matriz

    def ejecutar(self):
        pos_init_x, pos_init_y = np.where(self.matriz == 1)
        pos_end_x, pos_end_y = np.where(self.matriz == 2)

        nodo_inicial = Node(None, (pos_init_x[0], pos_init_y[0]))
        nodo_inicial.g = nodo_inicial.h = nodo_inicial.f = 0

        nodo_final = Node(None, (pos_end_x[0], pos_end_y[0]))
        nodo_final.g = nodo_final.h = nodo_final.f = 0

        lista_abierta = []
        lista_cerrada = []
        lista_abierta.append(nodo_inicial)

        while len(lista_abierta) > 0:
            nodo_actual = lista_abierta[0]
            indice_actual = 0

            for indice, nodo in enumerate(lista_abierta):
                if nodo.f < nodo_actual.f:
                    nodo_actual = nodo
                    indice_actual = indice

            lista_abierta.pop(indice_actual)
            lista_cerrada.append(nodo_actual)

            # Emitimos los estados que se encuentra la celda en ese momento: celda explorada, cerrada o abierta
            yield {
                "tipo": "explorando",
                "cerrada": nodo_actual.position,
                "abierta": [n.position for n in lista_abierta]
            }

            # Si el nodo actual es el objetivo, terminamos el algoritmo y mandamos el camino con su ruta
            if nodo_actual == nodo_final:
                camino = []
                nodo = nodo_actual
                while nodo is not None:
                    camino.append(nodo.position)
                    nodo = nodo.parent
                
                yield {
                    "tipo": "camino",
                    "camino": camino[::-1] # Invertido
                }
                return

            hijos = []
            for nueva_posicion in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                nodo_posicion = (nodo_actual.position[0] + nueva_posicion[0], nodo_actual.position[1] + nueva_posicion[1])

                if nodo_posicion[0] < 0 or nodo_posicion[0] >= self.dim or nodo_posicion[1] < 0 or nodo_posicion[1] >= self.dim:
                    continue
                if self.matriz[nodo_posicion[0]][nodo_posicion[1]] == -1:
                    continue

                nuevo_nodo = Node(nodo_actual, nodo_posicion)
                hijos.append(nuevo_nodo)

            for hijo in hijos:
                if hijo in lista_cerrada:
                    continue

                hijo.g = nodo_actual.g + 1
                hijo.h = abs(hijo.position[0] - nodo_final.position[0]) + \
                        abs(hijo.position[1] - nodo_final.position[1])
                hijo.f = hijo.g + hijo.h

                skip = False
                for nodo_abierto in lista_abierta:
                    if hijo == nodo_abierto and hijo.g >= nodo_abierto.g:
                        skip = True
                        break
                if skip:
                    continue

                lista_abierta.append(hijo)