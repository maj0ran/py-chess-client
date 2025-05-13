import pygame
from gui import GUIObject


BOARD_BLACK = "0x545357"
BOARD_WHITE = "0xf0e0d0"
BG = "0x8f5b26"


BLACK = 0x20
WHITE = 0x00

KING = 75
QUEEN = 81
ROOK = 82
BISHOP = 66
KNIGHT = 78
PAWN = 80

EMPTY = 88


class Square(GUIObject):
    def __init__(self, position, size, color):
        super().__init__(position, size)
        self.item.fill(color)
        self._cb = None  # callback function on click

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


class ChessGrid(GUIObject):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.selected = (0, 0)
        self.pos = position
        self.size = size[0]
        self.fields = list()

        # create map with the piece images
        self.res = {}
        self.res[EMPTY] = None,
        self.res[ROOK + WHITE] = pygame.image.load("res/r_w.png")
        self.res[ROOK + BLACK] = pygame.image.load("res/r_b.png")
        self.res[KNIGHT + WHITE] = pygame.image.load("res/n_w.png")
        self.res[KNIGHT + BLACK] = pygame.image.load("res/n_b.png")
        self.res[BISHOP + WHITE] = pygame.image.load("res/b_w.png")
        self.res[BISHOP + BLACK] = pygame.image.load("res/b_b.png")
        self.res[QUEEN + WHITE] = pygame.image.load("res/q_w.png")
        self.res[QUEEN + BLACK] = pygame.image.load("res/q_b.png")
        self.res[KING + WHITE] = pygame.image.load("res/k_w.png")
        self.res[KING + BLACK] = pygame.image.load("res/k_b.png")
        self.res[PAWN + WHITE] = pygame.image.load("res/p_w.png")
        self.res[PAWN + BLACK] = pygame.image.load("res/p_b.png")

        field_size = self.size / 8
        x = 0
        y = 0

        for xi in range(0, 8):
            for yi in range(0, 8):
                rect_x = x + (xi * field_size)
                rect_y = y + ((7 - yi) * field_size)
                if (xi + yi) % 2 == 0:
                    field_color = BOARD_BLACK
                else:
                    field_color = BOARD_WHITE
                square = Square((rect_x, rect_y),
                                (field_size, field_size), field_color)
                #    square.draw(self.item)
                self.fields.append(square)

    def get(self, pos: ()) -> int:
        return self.field[pos.x][pos.y]

    def set(self, pos: (), val: int):
        self.field[pos.x][pos.y] = val

    def get_res(self, val: int) -> pygame.Surface:
        return self.res[val]

    def get_field(self, x, y) -> ():
        x = x - self.pos.x
        y = y - self.pos.y

        if x < 0 or x > self.size or y < 0 or y > self.size:
            return None

        x = int(x / (self.size / 8))
        y = 7 - int(y / (self.size / 8))

        return (x, y)

    def select(self, x, y):
        self.selected = self.get_field(x, y)

    def move(self, src: (), dst: ()):
        piece = self.get(src)
        self.set(src, 0)
        self.set(dst, piece)

    def draw(self, screen):
        for f in self.fields:
            f.draw(self.item)
        screen.blit(self.item, self.hitbox)
