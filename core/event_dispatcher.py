import pygame

class EventDispatcher:
    def __init__(self):
        self._actions = []

    def register(self, button, callback):
        self._actions.append((button, callback))

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        for button, callback in self._actions:
            if button.is_clicked(event):
                result = callback()

                # Permitir retornar cambios de pantalla
                if result is not None:
                    return result

        return None