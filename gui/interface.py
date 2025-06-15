import pygame

from gui.scenes.main_scene import MainScene
from gui.scenes.chess_scene import ChessScene
from eventbus import AppEvent


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960


class UserInterface:
    def __init__(self, eventbus):
        self.bus = eventbus

        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Python Chess Client")

        size = self.surface.get_size()
        self.scenes = {
            "main": MainScene(size, eventbus),
            "ingame": ChessScene(size, eventbus)
        }
        self.bus.register(AppEvent.NEW_GAME, self.on_new_game)
        self.bus.register(AppEvent.SWITCH_SCENE, self.switch_scene)
        self.switch_scene("main")

        self.running = True

    def switch_scene(self, scene):
        new_scene = self.scenes.get(scene)
        if new_scene:
            self.active_scene = new_scene
        else:
            print(f"Error: Scene '{scene}' not found.")
            # Potentially fall back to a default scene or handle error

    # do what you want with the display like in any pygame code you write
    def draw(self, events, mouse_rel):
        self.surface.fill((50, 50, 50))
        self.active_scene.draw(events, mouse_rel)
        self.surface.blit(self.active_scene.surface, (0, 0))

    def run(self):
        while self.running:
            # dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            # --- Event Handling ---
            for event in pygame.event.get():
                self.active_scene.handle(event)

                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        self.running = False

                # Pass event to active scene
                if self.active_scene:
                    self.draw(None, None)

            pygame.display.flip()

        pygame.quit()

    def on_new_game(self, game_info):
        hoster = game_info.hoster_id
        game_id = game_info.game_id

        if hoster == 1:
            self.switch_scene("ingame")
