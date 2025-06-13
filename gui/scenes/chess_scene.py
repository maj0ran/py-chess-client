from . import BaseScene
import pygame
from gui import GUIObject, Image


class ChessLogic:
    def __init__(self):
        ...


"""
Ingame Scene with a chess board
"""


class Square(GUIObject):
    def __init__(self, position, size, color, x, y):
        super().__init__(position, (size, size))
        self.color = color
        self.item.fill(color)
        self.x = x
        self.y = y


class ChessScene(BaseScene):
    def __init__(self, size, eventbus):
        super().__init__(size, eventbus)

        self.board_x = 100
        self.board_y = 100
        self.board_size = 800
        self.init_chess_board((self.board_x, self.board_y), self.board_size)

        self.selected_square = None

    def get_square_coord(self, abs_x, abs_y) -> ():
        print("mouse coord:", abs_x, abs_y)
        if abs_x < self.board_x or abs_x > self.board_x + self.board_size or \
           abs_y < self.board_y or abs_y > self.board_y + self.board_size:
            return None

        x = abs_x - self.board_x
        y = abs_y - self.board_y

        x = int(x / (self.board_size / 8))
        y = 7 - int(y / (self.board_size / 8))

        return (x, y)

    def select(self, x, y):
        if self.selected_square is not None:
            if (self.selected_square.x + self.selected_square.y) % 2 == 0:
                self.selected_square.item.fill(BOARD_BLACK)
            else:
                self.selected_square.item.fill(BOARD_WHITE)

        square = self.elements[x * 8 + y]
        select_color = "0xff0000"
        self.selected_square = square
        square.item.fill(select_color)

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            coord = self.get_square_coord(event.pos[0], event.pos[1])
            if coord is not None:
                self.select(coord[0], coord[1])

    def init_chess_board(self, pos, size):
        square_size = size / 8
        x = pos[0]
        y = pos[1]

        for xi in range(0, 8):
            for yi in range(0, 8):
                rect_x = x + (xi * square_size)
                rect_y = y + ((7 - yi) * square_size)
                if (xi + yi) % 2 == 0:
                    square_color = BOARD_BLACK
                else:
                    square_color = BOARD_WHITE
                square = Square((rect_x, rect_y),
                                square_size, square_color, xi, yi)
                #    square.draw(self.item)
                self.add(square)

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

        img = Image((200, 200), (100, 100), self.res[ROOK + WHITE])
        self.add(img)


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


class ChessGrid(GUIObject):
    def __init__(self, position, size):
        ...

    def get(self, pos: ()) -> int:
        return self.field[pos.x][pos.y]

    def set(self, pos: (), val: int):
        self.field[pos.x][pos.y] = val

    def get_res(self, val: int) -> pygame.Surface:
        return self.res[val]

    def move(self, src: (), dst: ()):
        piece = self.get(src)
        self.set(src, 0)
        self.set(dst, piece)

    def draw(self, screen):
        for f in self.children:
            f.draw(self.item)
        screen.blit(self.item, self.hitbox)
