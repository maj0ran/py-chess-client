import pygame


class BaseScene:
    def __init__(self, size, eventbus):
        self.elements = list()
        self.bus = eventbus

        self.surface = pygame.Surface(
            size, pygame.SRCALPHA, 32)

    def add(self, e):
        self.elements.append(e)

    def draw(self, events, mouse_rel):
        for e in self.elements:
            e.draw(self.surface)

    def handle(self, event):
        for e in self.elements:
            if e.is_clicked(event):
                e.exec()
