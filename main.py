#!/bin/python

from gui.interface import UserInterface
from net import Client
from eventbus import EventBus, AppEvent
import asyncio

HOST = "127.0.0.1"
PORT = 7878


class Application:
    def __init__(self):
        self.bus = EventBus()
        self.ui = UserInterface(self.bus)
        self.net = Client(HOST, PORT, self.bus)

    def run(self):
        asyncio.run(self.net.run())
        self.ui.run()


WIN_WIDTH = 1280
WIN_HEIGHT = 960

# socket setup

# client = Client(HOST, PORT)
#
# client.send(bytes([10, 65, 32, 1]))
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
#                         grid.set((x, y), piece)


app = Application()

app.run()
