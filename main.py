#!/bin/python

from gui.interface import UserInterface
from net import Network
from eventbus import EventBus, AppEvent
from enum import Enum, auto


HOST = "127.0.0.1"
PORT = 7878


class ChessOpcode(Enum):
    """Defines the event types used in the application."""
    LOGIN = 0xF0
    GAME_CREATED = 0x81
    GAME_JOINED = 0x82
    BOARD_UPDATED = 0x83


class Application:
    def __init__(self):
        self.client_id = 0
        self.bus = EventBus()
        self.bus.register(AppEvent.MESSAGE_RECEIVED,
                          self.incoming_server_message)

        self.ui = UserInterface(self.bus)
        self.net = Network(HOST, PORT, self.bus)

    def run(self):
        try:
            # Start the non-blocking network thread.
            self.net.run()

        except KeyboardInterrupt:
            print("\n[Main] Program interrupted by user. Exiting.")
        finally:
            print("[Main] Application finished.")

        self.ui.run()

    def incoming_server_message(self):
        msg = self.net.recv_queue.get()
        print(f"application got network event: {msg}")
        self.parse_message(msg)

    def parse_message(self, msg):
        opcode = msg[0]
        print(f"got opcode: {opcode}")
        match ChessOpcode(opcode):
            case ChessOpcode.LOGIN:
                self.client_id = int.from_bytes(msg[1:5], "little")
                print(f"registered with client ID: {self.client_id}")

            case ChessOpcode.GAME_CREATED:
                game_id = int.from_bytes(msg[1:5], "little")
                client_id = int.from_bytes(msg[6:10], "little")
                print(
                    f"p[GOT GAME CREATED] game {game_id} from client {client_id}")

                if client_id == self.client_id:
                    data = [0x82, msg[1], msg[2], msg[3], msg[4], 0x20, 1]
                    self.bus.post(AppEvent.JOIN_GAME_REQUESTED, data=data)
            case ChessOpcode.GAME_JOINED:
                ...
            case ChessOpcode.BOARD_UPDATED:
                ...

        print("read full message")


class GameInfo:
    def __init__(self, game_id, hoster_id):
        self.game_id = game_id
        self.hoster_id = hoster_id


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
