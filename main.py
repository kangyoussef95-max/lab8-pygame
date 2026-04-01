import math
import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MIN_SQUARE_SIZE = 20
MAX_SQUARE_SIZE = 70
MIN_SPEED = 1.5
MAX_SPEED = 7.0
NUM_SQUARES = 100
FPS = 60
JITTER_ENABLED = True

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Random Moving Squares")
clock = pygame.time.Clock()


class Square:
    """Represents a square that moves randomly on the canvas."""

    def __init__(self, x: int, y: int, size: int) -> None:
        self.x = x
        self.y = y
        self.size = size

        # Bigger squares are slower.
        # Guard against divide-by-zero if min and max size are equal.
        if MAX_SQUARE_SIZE == MIN_SQUARE_SIZE:
            self.max_speed = MAX_SPEED
        else:
            size_ratio = (self.size - MIN_SQUARE_SIZE) / (MAX_SQUARE_SIZE - MIN_SQUARE_SIZE)
            self.max_speed = MAX_SPEED - size_ratio * (MAX_SPEED - MIN_SPEED)
            self.max_speed = min(self.max_speed, MAX_SPEED)
            self.max_speed = max(MIN_SPEED, self.max_speed)

        # Pick a random movement direction and a speed that does not exceed max_speed.
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(MIN_SPEED, self.max_speed)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        # Random color
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

    def should_apply_jitter(self) -> bool:
        """Stub: decide whether to jitter this frame or skip it."""
        # TODO: Return True/False based on your strategy (every frame, or every now and then).
        return random.random() < 0.1

    def compute_jitter_rotation(self) -> float:
        """Stub: return a small rotation angle in radians."""
        # TODO: Return a small random angle, e.g. between -max_angle and +max_angle.
        max_angle_degrees = 5.0
        return math.radians(random.uniform(-max_angle_degrees, max_angle_degrees))

    def rotate_velocity(self, angle_radians: float) -> None:
        """Stub: rotate (vx, vy) by angle_radians while preserving speed."""
        # TODO: Use a 2D rotation matrix to rotate self.vx/self.vy.
        # vx' = vx*cos(a) - vy*sin(a)
        # vy' = vx*sin(a) + vy*cos(a)
        cos_a = math.cos(angle_radians)
        sin_a = math.sin(angle_radians)

        new_vx = self.vx * cos_a - self.vy * sin_a
        new_vy = self.vx * sin_a + self.vy * cos_a

        self.vx = new_vx
        self.vy = new_vy

    def apply_jitter(self) -> None:
        """Stub: apply jitter as a small rotation of the speed vector."""
        if not JITTER_ENABLED:
            return

        # TODO: If should_apply_jitter() is True, compute angle and rotate velocity.
        # if self.should_apply_jitter():
        #     angle = self.compute_jitter_rotation()
        #     self.rotate_velocity(angle)
        if self.should_apply_jitter():
            angle = self.compute_jitter_rotation()
            self.rotate_velocity(angle)

    def clamp_speed(self) -> None:
        """Clamp total velocity magnitude so it does not exceed this square's max_speed."""
        speed = math.hypot(self.vx, self.vy)
        if speed > self.max_speed and speed > 0:
            scale = self.max_speed / speed
            self.vx *= scale
            self.vy *= scale

    def update(self) -> None:
        """Update the square's position and bounce off walls."""
        self.apply_jitter()
        self.clamp_speed()

        self.x += self.vx
        self.y += self.vy

        # Bounce off walls
        if self.x <= 0 or self.x + self.size >= WINDOW_WIDTH:
            self.vx = -self.vx
        if self.y <= 0 or self.y + self.size >= WINDOW_HEIGHT:
            self.vy = -self.vy

        # Keep square within bounds
        self.x = max(0, min(self.x, WINDOW_WIDTH - self.size))
        self.y = max(0, min(self.y, WINDOW_HEIGHT - self.size))

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the square on the given surface."""
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))


def main() -> None:
    """Main game loop."""
    sizes = [random.randint(MIN_SQUARE_SIZE, MAX_SQUARE_SIZE) for _ in range(NUM_SQUARES)]
    squares = [
        Square(
            size=size,
            x=random.randint(0, WINDOW_WIDTH - size),
            y=random.randint(0, WINDOW_HEIGHT - size),
        )
        for size in sizes
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for square in squares:
            square.update()

        screen.fill(WHITE)
        for square in squares:
            square.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()