#!/bin/python

import pygame
import socket
import sys
import time
from interface import Application


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


app = Application()
app.run()
# pygame setup
# pygame.init()
# display = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
# clock = pygame.time.Clock()
# running = True
#
# client = Client(HOST, PORT)
#
# client.send(bytes([10, 65, 32, 1]))
# select = (0, 0)
# grid = ChessGrid()
# while running:
#     # poll for events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 running = False
#
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             x = int(event.pos[0])
#             y = int(event.pos[1])
#
#             if (event.button == pygame.BUTTON_LEFT):
#                 grid.select(x, y)
#                 print("selected grid: ", grid.selected.x, grid.selected.y)
#
#             if (event.button == pygame.BUTTON_RIGHT):
#                 dest = grid.get_field(x, y)
#                 src = grid.selected
#                 b = [0xD, src.x + 97, src.y + 49, dest.x + 97, dest.y + 49]
#                 print("Sending chess move: " + chr(src.x + 97) +
#                       chr(src.y + 49) + chr(dest.x + 97) + chr(dest.y + 49) + "...")
#                 client.send(bytes(b))
#                 response = client.recv()
#                 if response is not None:
#                     for i in response:
#                         x = i[0] - 97
#                         y = i[1] - 49
#                         piece = i[2]
#
#                         print("setting: ", x, y, str(piece))
#
#                         grid.set(Pos(x, y), piece)
#
#     # clear screen
#     display.fill(BG)
#     bord_size = 800
#     pos = Pos(int(WIN_WIDTH) / 2 - int(bord_size / 2), 0)
#     grid.draw(pos, bord_size)
#
#     pygame.display.flip()
#     clock.tick(60)  # limits FPS to 60

pygame.quit()
