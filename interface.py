import pygame
from gui.button import Button
from chess import ChessGrid

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960


class BaseScene:
    def __init__(self, app):
        self.app = app
        self.elements = list()

        self.surface = pygame.Surface(
            app.surface.get_size(), pygame.SRCALPHA, 32)

    def add(self, e):
        self.elements.append(e)

    def draw(self, surface, events, mouse_rel):
        pass


class ChessScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        self.chess = ChessGrid((100, 100), (800, 800))

    def draw(self, surface, events, mouse_rel):
        self.chess.draw(surface)


class MainScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)

        create_game_btn = Button((300, 100), (200, 50),
                                 (200, 200, 200), "Create Game")

        create_game_btn.on_clicked(lambda: self.app.switch_scene("ingame"))
        join_game_btn = Button((600, 100), (200, 50),
                               (200, 200, 200), "Join Game")
        self.add(create_game_btn)
        self.add(join_game_btn)

    def draw(self, surface, events, mouse_rel):
        for e in self.elements:
            e.draw(self.surface)

    def create_game(self):
        ...


class Application:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.scenes = {}
        self.active_scene = None
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # bind screen to gui elements and set theme
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
            # dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds

            # --- Event Handling ---
            for event in pygame.event.get():
                for e in self.active_scene.elements:
                    if e.is_clicked(event):
                        e.exec()

                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        self.running = False

                # Pass event to active scene
                if self.active_scene:
                    self.surface.fill((0, 0, 0))  # Clear screen
                    self.draw(None, None)

            pygame.display.flip()

        pygame.quit()
