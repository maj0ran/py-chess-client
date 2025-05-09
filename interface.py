"""We show here how to let the user choose a value using another element."""


import pygame
import thorpy as tp
from chess import ChessGrid, Pos

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
        self.width = 1200
        self.height = 900
        self.surface = pygame.display.set_mode((self.width, self.height))

        tp.init(self.surface)  # bind screen to gui elements and set theme
        tp.set_style_attr("radius", 0.0)
        tp.set_style_attr("bck_color", (200, 200, 200))

        self.active_scene = MainMenuScene(self.surface)

    # do what you want with the display like in any pygame code you write
    def draw(self, events, mouse_rel):
        self.surface.fill((50, 50, 50))
        self.active_scene.draw(self.surface, events, mouse_rel)
    #  self.chess.draw(Pos(100, 100), 800)

    def run(self):
        clock = pygame.time.Clock()
        playing = True
        while playing:
            clock.tick(60)
            events = pygame.event.get()
            mouse_rel = pygame.mouse.get_rel()
            for e in events:
                if e.type == pygame.QUIT:
                    playing = False
                else:  # do your stuff with events
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_k:
                            create_game()
            self.draw(events, mouse_rel)  # do your stuff with display
            # update Thorpy elements and draw them
            pygame.display.flip()
        pygame.quit()


class MainMenuScene(BaseScene):
    def __init__(self, surface):
        btn_create_game = tp.Button("Create Game")
        btn_create_game.at_unclick = create_game

        btn_join_game = tp.Button("Join Game")
        btn_join_game.at_unclick = create_game
        iface = tp.Group([btn_create_game, btn_join_game], mode="h")
        iface.set_center(surface.get_width() / 2, 50)

        self.updater = iface.get_updater()

    def draw(self, surface, events, mouse_rel):
        self.updater.update(events=events, mouse_rel=mouse_rel)


class ChessScene:
    def __init__(self, app: Application):
        ...


class BaseScene:
    def __init__(self, app):
        self.app = app
        self.font = pygame.font.Font(None, 50)  # Generic font for scene titles

    def handle_event(self, event):
        """Handle a single event."""
        pass

    def update(self, dt):
        """Update scene state."""
        pass

    def draw(self, screen):
        """Draw scene content to the screen."""
        pass

    def on_enter(self):
        """Called when the scene becomes active."""
        print(f"Entering {self.__class__.__name__}")

    def on_exit(self):
        """Called when the scene is exited."""
        print(f"Exiting {self.__class__.__name__}")

# --- Concrete Scene Implementations ---


class SceneOne(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        self.title = "Scene One (Press 2 for Scene Two)"
        # List to store (type, color, rect, [optional_params])
        self.shapes = []

    def _generate_chess_board(self):

        BOARD_BLACK = "0x545357"
        BOARD_WHITE = "0xf0e0d0"
        BG = "0x8f5b26"
        size = 800
        pos = Pos(0, 0)
        width = self.surface.width
        height = self.surface.height
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

    def on_enter(self):
        super().on_enter()
        self._generate_chess_board()

    def draw(self, screen):
        # Draw title
        title_surface = self.font.render(self.title, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_surface, title_rect)

        # Draw shapes
        for shape_data in self.shapes:
            shape_type = shape_data[0]
            color = shape_data[1]

            if shape_type == "rect":
                rect = shape_data[2]
                pygame.draw.rect(screen, color, rect)
            elif shape_type == "circle":
                rect = shape_data[2]  # This is the bounding rect
                radius = shape_data[3]
                pygame.draw.circle(screen, color, rect.center, radius)
            elif shape_type == "polygon":
                points = shape_data[2]
                pygame.draw.polygon(screen, color, points)

        # Instructions
        instr_font = pygame.font.Font(None, 30)
        instr_text = "Press ESC to quit"
        instr_surf = instr_font.render(instr_text, True, WHITE)
        instr_rect = instr_surf.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(instr_surf, instr_rect)


class SceneTwo(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        self.title = "Scene Two (Press 1 for Scene One)"
        self.circles = []  # List to store (color, center_pos, radius)

    def _generate_interface(self):
        ...

    def on_enter(self):
        super().on_enter()
        self._generate_interface()

    def draw(self, screen):
        # Draw title
        title_surface = self.font.render(self.title, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_surface, title_rect)

        # Draw circles
        for color, pos, radius in self.circles:
            pygame.draw.circle(screen, color, pos, radius)

        # Instructions
        instr_font = pygame.font.Font(None, 30)
        instr_text = "Press ESC to quit"
        instr_surf = instr_font.render(instr_text, True, WHITE)
        instr_rect = instr_surf.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(instr_surf, instr_rect)
