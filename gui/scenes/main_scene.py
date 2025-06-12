from . import BaseScene
from gui.button import Button
from gui import Command

"""
Main menu to create and join games
"""


class MainScene(BaseScene):
    def __init__(self, size):
        super().__init__(size)

        create_game_btn = Button((300, 100), (200, 50),
                                 (200, 200, 200), "Create Game")
        create_game_btn.on_clicked(lambda: Command(["switch_scene", "ingame"]))

        join_game_btn = Button((600, 100), (200, 50),
                               (200, 200, 200), "Join Game")
        self.add(create_game_btn)
        self.add(join_game_btn)
