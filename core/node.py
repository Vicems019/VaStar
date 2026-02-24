class Node():
    def __init__(self, parent=None,position=None):
        self.parent = parent
        self.position = position
        
        self.g = 0  # Costo desde el nodo inicial hasta este nodo
        self.h = 0  # Costo heurístico desde este nodo hasta el nodo objetivo
        self.f = 0  # Costo total (g + h)

    def __eq__(self, other):
        return self.position == other.position