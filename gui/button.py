from . import GUIObject
import pygame


class Button(GUIObject):

    def __init__(self, position, size, color, text):
        super().__init__(position, size)
        self._cb = None  # callback function on click

        self.item.fill(color)

        font = pygame.font.SysFont(None, 32)
        text = font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(size[0] / 2, size[1] / 2))
        text_rect.fit

        self.item.blit(text, text_rect)
