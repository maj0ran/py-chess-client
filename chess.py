
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

        # Set all empty fields
        self.field = [[EMPTY for _ in range(8)] for _ in range(8)]

        self.field[0][0] = ROOK + WHITE
        self.field[7][0] = ROOK + WHITE
        self.field[0][7] = ROOK + BLACK
        self.field[7][7] = ROOK + BLACK
        self.field[1][0] = KNIGHT + WHITE
        self.field[6][0] = KNIGHT + WHITE
        self.field[1][7] = KNIGHT + BLACK
        self.field[6][7] = KNIGHT + BLACK
        self.field[2][0] = BISHOP + WHITE
        self.field[5][0] = BISHOP + WHITE
        self.field[2][7] = BISHOP + BLACK
        self.field[5][7] = BISHOP + BLACK
        self.field[3][0] = QUEEN + WHITE
        self.field[3][7] = QUEEN + BLACK
        self.field[4][7] = KING + BLACK
        self.field[4][0] = KING + WHITE

        for x in range(0, 8):
            self.field[x][1] = PAWN + WHITE
            self.field[x][6] = PAWN + BLACK

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
                rect = pygame.Rect(rect_x, rect_y, field_size, field_size)
                # empty fields
                if (xi + yi) % 2 == 0:
                    pygame.draw.rect(self.surface, BOARD_BLACK, rect)
                else:
                    pygame.draw.rect(self.surface, BOARD_WHITE, rect)

                # selected field
                if self.selected == Pos(xi, yi):
                    pygame.draw.rect(self.surface, "0x65a326", rect)

                # pieces
                if self.get(Pos(xi, yi)) != EMPTY:
                    res = self.get_res(self.get(Pos(xi, yi)))
                    self.surface.blit(res, (rect_x, rect_y))
