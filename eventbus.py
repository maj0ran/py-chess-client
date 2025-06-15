from collections import defaultdict
from enum import Enum, auto
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class AppEvent(Enum):
    """Defines the event types used in the application."""

    # network interface events
    JOIN_GAME_REQUESTED = auto()
    CREATE_GAME_REQUESTED = auto()
    MESSAGE_RECEIVED = auto()

    NEW_GAME = auto()

    # internal GUI events
    SWITCH_SCENE = auto()


class EventBus:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._listeners = defaultdict(list)
        print(self._listeners)
        self.logger.info("EventBus initialized.")

    def register(self, event: AppEvent, callback):
        """
        Register a callback for a specific event. The callback is stored as a
        weak reference, allowing its parent object to be garbage collected.
        """
        self._listeners[event].append(callback)
        self.logger.info(
            f"Registered {getattr(callback, '__qualname__', repr(callback))} for event {event.name}")

    def unregister(self, event: AppEvent, callback):
        """Unregister a callback for a specific event."""
        self._listeners[event].discard(
            callback)  # discard() doesn't raise an error if not found
        self.logger.info(
            f"Unregistered {getattr(callback, '__qualname__', repr(callback))}"
            f"from event {event.name}")

    def post(self, event: AppEvent, **kwargs):
        """Post an event to all registered listeners."""
        self.logger.info(
            f"Posting event {event.name} with data:, kwargs={kwargs}")
        for callback in self._listeners[event]:
            try:
                callback(**kwargs)
            except Exception as e:
                self.logger.error(
                    f"Error in callback for event {event.name}: {e}")
