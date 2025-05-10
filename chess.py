import pygame


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pos):
            return NotImplemented

        return (self.x == other.x) and (self.y == other.y)


FIELD_SIZE = 100
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


NO_POS = Pos(9, 9)


class Square():
    def __init__(self, position, size, color):
        self.item = pygame.Surface(size)  # the visual button
        self.item.fill(color)
        self.rect = pygame.Rect((0, 0), size)  # the hitbox for clicks
        self.rect.topleft = position
        self._cb = None  # callback function on click

    def draw(self, screen):
        screen.blit(self.item, self.rect)

    def is_clicked(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.rect.collidepoint(event.pos)

    def on_clicked(self, func):
        self._cb = func

    def exec(self):
        if self._cb is not None:
            self._cb()


class ChessGrid:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface.subsurface(pygame.Rect(100, 100, 800, 800))
        self.selected = Pos(0, 0)
        self.pos = Pos(0, 0)
        self.size = 0

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

    def get(self, pos: Pos) -> int:
        return self.field[pos.x][pos.y]

    def set(self, pos: Pos, val: int):
        self.field[pos.x][pos.y] = val

    def get_res(self, val: int) -> pygame.Surface:
        return self.res[val]

    def get_field(self, x, y) -> Pos:
        x = x - self.pos.x
        y = y - self.pos.y

        if x < 0 or x > self.size or y < 0 or y > self.size:
            return NO_POS

        x = int(x / (self.size / 8))
        y = 7 - int(y / (self.size / 8))

        return Pos(x, y)

    def select(self, x, y):
        self.selected = self.get_field(x, y)

    def move(self, src: Pos, dst: Pos):
        if src == NO_POS or dst == NO_POS:
            return

        piece = self.get(src)
        self.set(src, 0)
        self.set(dst, piece)

    def draw(self, pos: Pos, size: int):
        width = self.surface.width
        height = self.surface.height
        self.size = size
        x = pos.x
        y = pos.y
        if x + size > width:
            size = width - x
        if y + size > height:
            size = height - y

        if size < 80:
            size = 80

        # chess board has 8x8 fields, we make it easy
        # so that we can't render uneven looking boards
        size -= size % 8

        field_size = int(size / 8)

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
                square.draw(self.surface)
