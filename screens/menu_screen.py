import pygame

from ui.colors import Colors

WIDTH = 1280
HEIGHT = 720

size_input = pygame.Rect((WIDTH-260)//2, HEIGHT//2, 140, 40)
size_button = pygame.Rect((WIDTH+60)//2, HEIGHT//2, 100, 40)


class MenuScreen:

    def __init__(self, screen):
        self.screen = screen
        self.font_little = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 20)
        self.font_default = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 32)
        self.font_title = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 52)

        self.dim_text = ""
        self.active = False

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
                if size_input.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

                if size_button.collidepoint(event.pos):
                    try:
                        if int(self.dim_text) > 0:
                            dim = int(self.dim_text)
                            return ("game", [dim])
                    except:
                        pass

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.dim_text = self.dim_text[:-1]                
            elif event.unicode.isdigit():
                if len(self.dim_text) < 2:
                    self.dim_text += event.unicode
        return None, None

    def show(self):
        self.screen.fill(Colors.GRAY_LIGHT)

        text_main = self.font_title.render("Bienvenido a VaStar*", True, (0, 0, 0))
        self.screen.blit(text_main, (130, 100))

        input_color = Colors.GRAY_DARK if self.active else Colors.GRAY

        pygame.draw.rect(self.screen, input_color, size_input, border_radius=10)
        surface_text = self.font_default.render(self.dim_text, True, (0, 180, 180))
        self.screen.blit(surface_text, (size_input.x + 10, size_input.y + 5))

        pygame.draw.rect(self.screen, (0, 120, 200), size_button, border_radius=5)
        button_text = self.font_default.render("OK", True, Colors.WHITE)
        self.screen.blit(button_text, (size_button.x + 20, size_button.y + 5))

        self.set_dimensiones(self.dim_text)

    def set_dimensiones(self, value):
        mensaje = (
            "Introduce un número"
            if value == ""
            else f"Dimensiones del mapa {value}x{value}"
        )

        x = 320 if value == "" else 240

        message_surface = self.font_default.render(mensaje, True, Colors.BLACK)

        self.screen.blit(message_surface, (x, 280))