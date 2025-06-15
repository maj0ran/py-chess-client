import threading
import queue
from eventbus import AppEvent
import asyncio


class Network:
    """Handles async network communication to a server."""

    def __init__(self, host, port, eventbus):
        self.host = host
        self.port = port
        # Create the thread-safe queues for communication
        self.recv_queue = queue.Queue()
        self.send_queue = queue.Queue()

        self.bus = eventbus
        self.bus.register(AppEvent.CREATE_GAME_REQUESTED, self.send)
        self.bus.register(AppEvent.JOIN_GAME_REQUESTED, self.send)

    def run(self):
        thread = threading.Thread(target=self._run_async_loop, daemon=True)
        thread.start()
        print("[Net] Network thread started.")

    def send(self, data: []):
        length = len(data)
        print(f"[Net] sending {str(length)} bytes.")
        msg = length.to_bytes(1, 'big') + bytes(data)
        self.send_queue.put(msg)

    def _run_async_loop(self):
        """Runs the asyncio event loop in the new thread."""
        try:
            asyncio.run(self._main_coro())
        except Exception as e:
            print(f"[Net] CRITICAL: Async loop failed: {e}")

    async def _main_coro(self):
        """The main coroutine: connects and handles communication."""
        while True:  # Main reconnect loop
            try:
                print(
                    f"[Net] Attempting to connect to"
                    f"{self.host}:{self.port}...")
                reader, writer = await asyncio.open_connection(
                    self.host, self.port)
                print("[Net] Connection established successfully.")

                # Run two tasks concurrently:
                # one for receiving, one for sending.
                # If one task fails (e.g., due to disconnection), the other
                # will be cancelled, and the `gather` will raise an exception.
                await asyncio.gather(
                    self._receiver(reader),
                    self._sender(writer)
                )

            except (ConnectionRefusedError,
                    ConnectionResetError,
                    OSError) as e:
                print(f"[Net] Connection failed or was lost: {e}")
            except Exception as e:
                print(
                    f"[Net] An unexpected error "
                    f"occurred in network tasks: {e}")
            finally:
                print("[Net] Disconnected. "
                      "Will attempt to reconnect in 5 seconds...")
                await asyncio.sleep(5)

    async def _receiver(self, reader: asyncio.StreamReader):
        """Coroutine to continuously read data from the server."""
        while True:
            length = 0
            message = []
            while True:  # until full message got received
                # we first read the length, then we read
                # until {length} bytes are read
                length = await reader.read(1)
                if not length:
                    # empty read == connection closed
                    print("[Net] Server closed the connection.")
                    # Raising an exception will break the gather
                    # and trigger reconnect
                    raise ConnectionError("Server closed the connection")
                length = length[0]
                data = await reader.read(length)
                message += data
                if len(message) == length:
                    break

            print(f"received {message}")
            # Put the received message into the thread-safe queue for the UI
            self.recv_queue.put(message)
            self.bus.post(AppEvent.MESSAGE_RECEIVED)

    async def _sender(self, writer: asyncio.StreamWriter):
        """Coroutine to continuously check the outgoing queue and send data."""
        while True:
            try:
                message = self.send_queue.get_nowait()
                print(f"[Net] Sending from queue: '{message.strip()}'")
                writer.write(message)
                await writer.drain()
            except queue.Empty:
                # Queue is empty, yield control to the event loop.
                await asyncio.sleep(0.01)
            # If we get a connection error during send, we break the loop
            # and let the main coroutine handle the reconnection.
            except ConnectionError:
                print("[Net] Connection lost (sender).")
                break  # Exit the sender loop
