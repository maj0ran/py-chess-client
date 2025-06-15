from . import BaseScene
from gui.button import Button
from eventbus import AppEvent

"""
Main menu to create and join games
"""


class MainScene(BaseScene):
    def __init__(self, size, eventbus):
        super().__init__(size, eventbus)

        create_game_btn = Button((300, 100), (200, 50),
                                 (200, 200, 200), "Create Game")
        create_game_btn.on_clicked(self.create_game)

        join_game_btn = Button((600, 100), (200, 50),
                               (200, 200, 200), "Join Game")
        self.add(create_game_btn)
        self.add(join_game_btn)

    def create_game(self):
        self.bus.post(AppEvent.CREATE_GAME_REQUESTED,
                      data=[
                          10, 65, 32, 88,
                          2, 0, 0, 32,
                          3, 0, 0, 0])
