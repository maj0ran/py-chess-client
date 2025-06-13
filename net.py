import socket
from eventbus import AppEvent
import select


class Client:
    def __init__(self, HOST, PORT, eventbus):
        self.bus = eventbus

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        self.socket.settimeout(1.0)
        self.bus.register(AppEvent.CREATE_GAME_REQUESTED, self.send)

    def send(self, data: []):
        length = len(data)
        print("sending " + str(length) + " bytes.")
        self.socket.sendall(length.to_bytes(1, 'big'))
        self.socket.sendall(bytes(data))

    async def recv(self):
        print("waiting for response...")

        r, w, e = select.select([self.socket], [], [], 1)
        if self.socket in r:
            print("getting data...")
            length = self.socket.recv(1)
            length = int.from_bytes(length, 'big')
            print("waiting for " + str(length) + " bytes...")
            content = self.socket.recv(length)
            print("received " + str(len(content)) + " bytes.")
            print("content: " + str(content))
      #     changes = []
      #     if length == 0:
      #         return
      #     for i in range(1, length, 3):
      #         x = content[i]
      #         y = content[i + 1]
      #         piece = content[i + 2]
      #         changes.append((x, y, piece))

      #     print("list of changes: ", changes)
      # return changes

    async def run(self):
        while (True):
            self.recv()
