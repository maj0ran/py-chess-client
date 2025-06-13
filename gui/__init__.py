import pygame


class Command:
    def __init__(self, param: []):
        self.param = param


class GUIObject:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.item = pygame.Surface(size)
        self.hitbox = pygame.Rect(pos, size)
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
            return self._cb()


class Image(GUIObject):
    def __init__(self, pos, size, img):
        super().__init__(pos, size)
        self.img = img

    def draw(self, screen):
        screen.blit(self.img, self.pos)
