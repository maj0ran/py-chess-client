#!/bin/python

from interface import Application, ChessScene, MainScene
from net import Client

WIN_WIDTH = 1280
WIN_HEIGHT = 960

# socket setup
HOST = "127.0.0.1"
PORT = 7878

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
#                         grid.set(Pos(x, y), piece)


app = Application()

# Create and add scenes
ingame_scene = ChessScene(app)
main_menu = MainScene(app)

app.add_scene("main", main_menu)
app.add_scene("ingame", ingame_scene)

# Set initial scene
app.switch_scene("main")

app.run()
