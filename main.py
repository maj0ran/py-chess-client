#!/bin/python

import pygame
import socket
import sys
import time

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

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pos):
            return NotImplemented

        return (self.x == other.x) and (self.y == other.y)


NO_POS = Pos(9, 9)


class ChessGrid:
    def __init__(self):

        self.selected = Pos(0, 0)
        self.pos = Pos(0, 0)
        self.size = 0

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

        self.field = [[EMPTY for _ in range(8)] for _ in range(8)] # Set all empty fields

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

        piece = grid.get(src)
        grid.set(src, 0)
        grid.set(dst, piece)

    def draw(self, pos: Pos, size: int):
        self.pos = pos
        self.size = size
        x = pos.x
        y = pos.y
        if x + size > WIN_WIDTH:
            size = WIN_WIDTH - x
        if y + size > WIN_HEIGHT:
            size = WIN_HEIGHT - y

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
                    pygame.draw.rect(display, BOARD_BLACK, rect)
                else:
                    pygame.draw.rect(display, BOARD_WHITE, rect)

                # selected field
                if self.selected == Pos(xi, yi):
                    pygame.draw.rect(display, "0x65a326", rect)

                # pieces
                if grid.get(Pos(xi, yi)) != EMPTY:
                    res = grid.get_res(grid.get(Pos(xi, yi)))
                    display.blit(res, (rect_x, rect_y))


WIN_WIDTH = 1280
WIN_HEIGHT = 960

# socket setup
HOST = "127.0.0.1"
PORT = 7878


class Client:
    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        pass

    def send(self, data: []):
        length = len(data)
        print("sending " + str(length) + " bytes.")
        self.socket.sendall(length.to_bytes(1, 'big'))
        self.socket.sendall(bytes(data))

    def recv(self):
        self.socket.setblocking(True)
        print("waiting for response...")
        length = self.socket.recv(1)
        length = int.from_bytes(length, 'big')
        print("waiting for " + str(length) + " bytes...")
        content = self.socket.recv(length)
        print("received " + str(len(content)) + " bytes.")
        print("content: " + str(content))
        changes = []
        if length == 0:
            return
        for i in range(1, length, 3):
            x = content[i]
            y = content[i + 1]
            piece = content[i + 2]
            changes.append((x, y, piece))

        print("list of changes: ", changes)
        return changes


# pygame setup
pygame.init()
display = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()
running = True

client = Client(HOST, PORT)

client.send(bytes([10, 32, 65, 32, 1]))
select = (0, 0)
grid = ChessGrid()
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x = int(event.pos[0])
            y = int(event.pos[1])

            if (event.button == pygame.BUTTON_LEFT):
                grid.select(x, y)
                print("selected grid: ", grid.selected.x, grid.selected.y)

            if (event.button == pygame.BUTTON_RIGHT):
                dest = grid.get_field(x, y)
                src = grid.selected
                b = [0xD, 0x20, src.x + 97, src.y + 49, dest.x + 97, dest.y + 49]
                print("Sending chess move: " + chr(src.x + 97) +
                      chr(src.y + 49) + chr(dest.x + 97) + chr(dest.y + 49) + "...")
                client.send(bytes(b))
                response = client.recv()
                if response is not None:
                    for i in response:
                        x = i[0] - 97
                        y = i[1] - 49
                        piece = i[2]

                        print("setting: ", x, y, str(piece))

                        grid.set(Pos(x, y), piece)

    # clear screen
    display.fill(BG)
    bord_size = 800
    pos = Pos(int(WIN_WIDTH) / 2 - int(bord_size / 2), 0)
    grid.draw(pos, bord_size)

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
