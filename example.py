import pygame
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
COLORS = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]

# --- Base Scene Class ---


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

    def _generate_random_shapes(self, num_shapes=10):
        self.shapes = []
        for _ in range(num_shapes):
            shape_type = random.choice(["rect", "circle", "polygon"])
            color = random.choice(COLORS)
            x = random.randint(50, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 100)

            if shape_type == "rect":
                w = random.randint(20, 80)
                h = random.randint(20, 80)
                self.shapes.append(("rect", color, pygame.Rect(x, y, w, h)))
            elif shape_type == "circle":
                radius = random.randint(10, 40)
                self.shapes.append(("circle", color, pygame.Rect(
                    x, y, radius*2, radius*2), radius))  # Store rect for bounds
            elif shape_type == "polygon":
                num_points = random.randint(3, 6)
                points = []
                for _ in range(num_points):
                    offset_x = random.randint(-30, 30)
                    offset_y = random.randint(-30, 30)
                    points.append((x + offset_x, y + offset_y))
                self.shapes.append(("polygon", color, points))

    def on_enter(self):
        super().on_enter()
        self._generate_random_shapes(random.randint(5, 15))

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

    def _generate_random_circles(self, num_circles=20):
        self.circles = []
        for _ in range(num_circles):
            color = random.choice(COLORS)
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(100, SCREEN_HEIGHT - 50)
            radius = random.randint(5, 30)
            self.circles.append((color, (x, y), radius))

    def on_enter(self):
        super().on_enter()
        self._generate_random_circles(random.randint(10, 25))

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


# --- Application Class ---
class Application:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Scene Manager Demo")
        self.clock = pygame.time.Clock()
        self.running = True

        self.scenes = {}
        self.active_scene = None

    def add_scene(self, scene_name, scene_instance):
        self.scenes[scene_name] = scene_instance

    def switch_scene(self, scene_name):
        if self.active_scene:
            self.active_scene.on_exit()

        new_scene = self.scenes.get(scene_name)
        if new_scene:
            self.active_scene = new_scene
            self.active_scene.on_enter()
        else:
            print(f"Error: Scene '{scene_name}' not found.")
            # Potentially fall back to a default scene or handle error

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds

            # --- Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Global key presses for scene switching
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_1:
                        self.switch_scene("scene1")
                    elif event.key == pygame.K_2:
                        self.switch_scene("scene2")
                    # Add more keys for more scenes here

                # Pass event to active scene
                if self.active_scene:
                    self.active_scene.handle_event(event)

            # --- Update ---
            if self.active_scene:
                self.active_scene.update(dt)

            # --- Drawing ---
            self.screen.fill(BLACK)  # Clear screen
            if self.active_scene:
                self.active_scene.draw(self.screen)

            pygame.display.flip()

        pygame.quit()


# --- Main Execution ---
if __name__ == '__main__':
    app = Application()

    # Create and add scenes
    scene1 = SceneOne(app)
    scene2 = SceneTwo(app)

    app.add_scene("scene1", scene1)
    app.add_scene("scene2", scene2)

    # Set initial scene
    app.switch_scene("scene1")

    app.run()
