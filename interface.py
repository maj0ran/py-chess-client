"""We show here how to let the user choose a value using another element."""


import pygame
from pygame import Surface
import thorpy as tp
from chess import ChessGrid, Pos

FPS = 60
BLACK = 0x20
WHITE = 0x00
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900


def create_game():
    prompt = tp.TextInput("", "Enter game mode")
    alert = tp.AlertWithChoices(
        "Create Game", choices=["Ok", "Cancel"], children=[prompt])
    alert.launch_alone(self.draw)
    if alert.choice == "Cancel":
        ...  # do what you want, like nothing.
    elif alert.choice == "Ok":
        ...


class Application:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.scenes = {}
        self.active_scene = None
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # bind screen to gui elements and set theme
        tp.init(self.surface, tp.theme_classic)
        tp.set_style_attr("radius", 0.0)
        tp.set_style_attr("bck_color", (200, 200, 200))
        pygame.display.set_caption("Scene Manager Demo")

        self.running = True

    def add_scene(self, scene_name, scene_instance):
        self.scenes[scene_name] = scene_instance

    def switch_scene(self, scene_name):

        new_scene = self.scenes.get(scene_name)
        if new_scene:
            self.active_scene = new_scene
        else:
            print(f"Error: Scene '{scene_name}' not found.")
            # Potentially fall back to a default scene or handle error

    # do what you want with the display like in any pygame code you write
    def draw(self, events, mouse_rel):
        self.surface.fill((50, 50, 50))
        self.active_scene.draw(self.surface, events, mouse_rel)
        self.surface.blit(self.active_scene.surface, (0, 0))
    #  self.chess.draw(Pos(100, 100), 800)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds

            # --- Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_1:
                        self.switch_scene("scene1")
                    elif event.key == pygame.K_2:
                        self.switch_scene("scene2")

                # Pass event to active scene
                if self.active_scene:
                    self.surface.fill(BLACK)  # Clear screen
                    self.draw(None, None)

            pygame.display.flip()

        pygame.quit()


class BaseScene:
    def __init__(self, app):
        self.app = app
        self.surface = pygame.Surface(
            app.surface.get_size(), pygame.SRCALPHA, 32)

    def draw(self, surface, events, mouse_rel):
        """Draw scene content to the screen."""
        pass

# --- Concrete Scene Implementations ---


class ChessScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        self.title = "Scene One (Press 2 for Scene Two)"
        # List to store (type, color, rect, [optional_params])
        self.shapes = []

    def _generate_chess_board(self):

        BOARD_BLACK = "0x545357"
        BOARD_WHITE = "0xf0e0d0"
        size = 800
        pos = Pos(0, 0)
        width = SCREEN_WIDTH
        height = SCREEN_HEIGHT
        self.size = size
        x = pos.x
        y = pos.y
        if x + size > width:
            size = width - x
        if y + size > height:
            size = height - y

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
                    pygame.draw.rect(self.surface, BOARD_BLACK, rect)
                else:
                    pygame.draw.rect(self.surface, BOARD_WHITE, rect)

    def draw(self, surface, events, mouse_rel):
        self._generate_chess_board()


class MainScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        btn_create_game = tp.Button("Create Game")
        btn_create_game.at_unclick = create_game

        btn_join_game = tp.Button("Join Game")
        btn_join_game.at_unclick = create_game
        iface = tp.Group([btn_create_game, btn_join_game], mode="h")
        iface.set_center(app.surface.get_width() / 2, 50)

        self.updater = iface.get_updater()

    def draw(self, surface, events, mouse_rel):
        self.updater.update(events=events, mouse_rel=mouse_rel)
