import pygame
from ui.colors import Colors

class Button:
    def __init__(self, rect, base_color, hover_color, text="", font=None, text_color=Colors.WHITE,
                 border_radius=10, icon=None, border = None):
        self.rect = pygame.Rect(rect)
        self.base_color = base_color
        self.hover_color = hover_color
        self.text = text
        self.font = font
        self.text_color = text_color
        self.border_radius = border_radius
        self.icon = icon
        self.active = False
        self.border = border

    def draw(self, screen, mouse_pos):
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)

        if self.icon:
            icon_rect = self.icon.get_rect(center=self.rect.center)
            screen.blit(self.icon, icon_rect)

        if self.text and self.font:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

        if self.active and self.border:
            pygame.draw.rect(
                screen,
                Colors.BLACK,
                self.rect,
                4,
                border_radius=self.border_radius
            )

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                return True
            
            self.active = False
        return False