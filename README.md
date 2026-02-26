# 🚗 VaStar — A\* Pathfinding Simulator

> Prototipo de navegación autónoma urbana basado en el algoritmo A\* desarrollado en Python como proyecto formativo para el módulo de **Programación de Inteligencia Artificial**.

---

## 📋 Descripción

**VaStar** es un simulador interactivo de búsqueda de rutas óptimas que implementa el algoritmo de búsqueda heurística **A\*** sobre un mapa en forma de cuadrícula que representa una ciudad. El usuario puede diseñar el entorno, definir zonas transitables y bloqueadas, establecer puntos de origen y destino, y visualizar en tiempo real la ruta calculada por el algoritmo.

El proyecto simula el contexto de un **Programador Junior** en una empresa de avances tecnológicos automovilísticos, encargado de prototipar algoritmos de búsqueda de rutas para un sistema de navegación autónomo.

---

## ✨ Características

- 🗺️ **Mapa interactivo en cuadrícula** — Configurable en tamaño y distribución.
- 🚧 **Zonas bloqueadas y transitables** — Simula edificios, calles y áreas cerradas.
- 🔄 **Movimiento diagonal y en zig-zag** — No está limitado al formato Manhattan.
- 🎯 **Modo interactivo** — El usuario selecciona el punto de inicio y el destino.
- 🛣️ **Visualización de la ruta** — El camino calculado se muestra sobre el mapa resultante.
---

## 🧠 ¿Cómo funciona A\*?

A\* es un algoritmo de búsqueda informada que evalúa cada nodo usando la función:

```
f(n) = g(n) + h(n)
```

| Variable | Significado |
|----------|-------------|
| `g(n)` | Coste real acumulado desde el nodo inicial hasta `n` |
| `h(n)` | Heurística — estimación del coste desde `n` hasta el destino |
| `f(n)` | Coste total estimado del camino a través de `n` |

La heurística utilizada en este proyecto es la **distancia euclidiana**, lo que permite movimiento diagonal. Esto lo diferencia de la heurística de Manhattan, que sólo permite movimiento en los 4 ejes cardinales.

---

## 🚀 Instalación y ejecución

### Requisitos

- Python 3.8 o superior
- Librerías: `matplotlib`, `numpy`, `pygame` *(estándar)*

## 🗂️ Estructura del proyecto

```
VaStar/
│
├── VaStar.py               # Punto de entrada del programa
├── assets
    ├── PressStart2P-Regular.ttf  # fuente de texto
    ├── icons                     # Repositorio de iconos
├── core
    ├── astar.py                  # Lógica del programa
    ├── event_dispatcher.py       # Manejo de eventos (button)
    ├── node.py                   # Objeto Node
├── screens
    ├── menu_screen.py            # Ventana inicial
    ├── game_screen.py            # Ventana del juego
├── ui
    ├── button.py                 # Interfaz de botones
    ├── colors.py                 # Interfaz de colores
    ├── popup.py                  # Interfaz de ventanas emergentes
    ├── ui_actions.py             # Acciones de las interfaces
└── README.md
```

---

## 🎮 Uso

1. Ejecuta el programa y se mostrará el mapa inicial.
2. Ingresa la cantidad de dimensiones y Clickea en el boton "OK".
3. Selecciona el inicio, el final y los obstáculos en el mapa.
4. Pulsa "Ejecutar" para comenzar con el algoritmo.
5. Observa el resultado y repite el proceso con otros parámetros.
---

## 📊 Comparativa de algoritmos

| Algoritmo | Óptimo | Completo | Heurística | Velocidad (estimada) |
|-----------|--------|----------|------------|----------------------|
| **A\***       | ✅ Sí  | ✅ Sí    | ✅ Sí      | ⚡ Alta              |
| Dijkstra  | ✅ Sí  | ✅ Sí    | ❌ No      | 🐢 Media             |
| BFS       | ✅ Sí* | ✅ Sí    | ❌ No      | 🐢 Baja              |
| Greedy Best-First | ❌ No | ✅ Sí | ✅ Sí   | ⚡ Muy alta          |

> \* BFS es óptimo sólo cuando todos los costes son iguales.

A\* destaca sobre Dijkstra porque reduce el número de nodos explorados gracias a la heurística, y sobre Greedy Best-First porque garantiza encontrar el camino más corto.

---

## 📚 Fases del proyecto

### 🔍 Fase 1 — Investigación
Estudio del algoritmo A\*, su historia, estructura matemática y aplicaciones reales. También aprender e investigar las distintas funcionalidades que ofrece pygame.

### ⚙️ Fase 2 — Producción
Implementación en Python con representación visual interactiva del mapa y la ruta calculada.

### 📝 Fase 3 — Memoria
Documentación del proceso, decisiones de diseño, resultados y comparativa con otros algoritmos de búsqueda.

---

## 👤 Autor

**Vicente Marín Suazo**  

Curso: Programación de Inteligencia Artificial y Big Data

Centro: Cámara de Comercio de Sevilla

---
