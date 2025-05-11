import pygame


class GUIObject():
    def __init__(self, pos, size):
        self.item = pygame.Surface(size)
        self.hitbox = pygame.Rect((0, 0), size)
        self.hitbox.topleft = pos

    def draw(self, screen):
        screen.blit(self.item, self.hitbox)

    def is_clicked(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.hitbox.collidepoint(event.pos)

    def on_clicked(self, func):
        self._cb = func

    def exec(self):
        if self._cb is not None:
            self._cb()
