import pygame

from gui.scenes.main_scene import MainScene
from gui.scenes.chess_scene import ChessScene
from gui import Command

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960


class Application:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Python Chess Client")

        size = self.surface.get_size()
        self.scenes = {
            "main": MainScene(size),
            "ingame": ChessScene(size)
        }
        self.switch_scene("main")

        self.running = True

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
        self.active_scene.draw(events, mouse_rel)
        self.surface.blit(self.active_scene.surface, (0, 0))

    def run(self):
        while self.running:
            # dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds

            # --- Event Handling ---
            for event in pygame.event.get():
                cmd = self.active_scene.handle(event)

                # switching scenes is done by the app so we have to do it here
                if type(cmd) is Command:
                    if cmd.param[0] == "switch_scene":
                        self.switch_scene(cmd.param[1])

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
