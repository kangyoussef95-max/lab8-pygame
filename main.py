import math
import pygame
import random
from dataclasses import dataclass

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MIN_SQUARE_SIZE = 20
MAX_SQUARE_SIZE = 70
MIN_SPEED = 1.5
MAX_SPEED = 7.0
NUM_SQUARES = 20
FPS = 60
JITTER_ENABLED = True
FLEE_RADIUS = 150
FLEE_STRENGTH = 0.25
BASELINE_FPS = 60.0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Random Moving Squares")
clock = pygame.time.Clock()


@dataclass(frozen=True)
class SquareSnapshot:
    """Immutable snapshot of a square for a single frame."""
    owner: "Square"
    x: float
    y: float
    size: int


class Square:
    """Represents a square that moves randomly on the canvas."""

    def __init__(self, x: int, y: int, size: int) -> None:
        self.x = float(x)
        self.y = float(y)
        self.size = size

        # Bigger squares are slower.
        # Guard against divide-by-zero if min and max size are equal.
        if MAX_SQUARE_SIZE == MIN_SQUARE_SIZE:
            self.max_speed = MAX_SPEED
        else:
            size_ratio = (self.size - MIN_SQUARE_SIZE) / (
                MAX_SQUARE_SIZE - MIN_SQUARE_SIZE
            )
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

    def snapshot(self) -> SquareSnapshot:
        """Capture the square state so all updates use the same frame data."""
        return SquareSnapshot(owner=self, x=self.x, y=self.y, size=self.size)

    def should_apply_jitter(self, delta_time: float) -> bool:
        """Stub: decide whether to jitter this frame or skip it."""
        # TODO: Return True/False based on your strategy (every frame, or every now and then).
        if delta_time <= 0:
            return False

        # Keep the original 10% chance at 60 FPS, but make it time-scaled.
        frame_scale = delta_time * BASELINE_FPS
        chance_this_frame = 1 - (1 - 0.1) ** frame_scale
        return random.random() < chance_this_frame

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

    def apply_jitter(self, delta_time: float) -> None:
        """Stub: apply jitter as a small rotation of the speed vector."""
        if not JITTER_ENABLED:
            return

        # TODO: If should_apply_jitter() is True, compute angle and rotate velocity.
        # if self.should_apply_jitter():
        #     angle = self.compute_jitter_rotation()
        #     self.rotate_velocity(angle)
        if self.should_apply_jitter(delta_time):
            angle = self.compute_jitter_rotation()
            self.rotate_velocity(angle)

    def clamp_speed(self) -> None:
        """Clamp total velocity magnitude so it does not exceed this square's max_speed."""
        speed = math.hypot(self.vx, self.vy)
        if speed > self.max_speed and speed > 0:
            scale = self.max_speed / speed
            self.vx *= scale
            self.vy *= scale

    def apply_fleeing(self, all_squares: list[SquareSnapshot], delta_time: float) -> None:
        """Stub: push this square away from nearby larger squares."""
        # TODO: Compute the center of this square.
        # center_x = self.x + self.size / 2
        # center_y = self.y + self.size / 2
        center_x = self.x + self.size / 2
        center_y = self.y + self.size / 2

        closest_distance = FLEE_RADIUS + 1
        closest_flee_x = 0.0
        closest_flee_y = 0.0
        closest_size_difference = 0.0

        # TODO: Loop through all_squares and skip self.
        # for other in all_squares:
        #     if other is self:
        #         continue
        for other in all_squares:
            if other.owner is self:
                continue

            # TODO: Ignore squares that are the same size or smaller.
            # if other.size <= self.size:
            #     continue
            if other.size <= self.size:
                continue

            # TODO: Compute dx, dy, and distance between square centers.
            # dx = center_x - other_center_x
            # dy = center_y - other_center_y
            # distance = math.hypot(dx, dy)
            other_center_x = other.x + other.size / 2
            other_center_y = other.y + other.size / 2
            dx = center_x - other_center_x
            dy = center_y - other_center_y
            distance = math.hypot(dx, dy)

            # TODO: Only consider threats within FLEE_RADIUS.
            # if distance > FLEE_RADIUS:
            #     continue
            if distance > FLEE_RADIUS:
                continue

            # TODO: Handle distance == 0 with a tiny random direction.
            # if distance == 0:
            #     # pick a small random vector and normalize it
            #     pass
            if distance == 0:
                flee_x = random.uniform(-1, 1)
                flee_y = random.uniform(-1, 1)
                random_length = math.hypot(flee_x, flee_y)

                while random_length < 0.0001:
                    flee_x = random.uniform(-1, 1)
                    flee_y = random.uniform(-1, 1)
                    random_length = math.hypot(flee_x, flee_y)

                flee_x /= random_length
                flee_y /= random_length
            else:
                flee_x = dx / distance
                flee_y = dy / distance

            # TODO: Track the closest threat and remember its flee direction.
            if distance < closest_distance:
                closest_distance = distance
                closest_flee_x = flee_x
                closest_flee_y = flee_y
                closest_size_difference = other.size - self.size

        # TODO: Use the closest threat to compute flee strength.
        # strength = ...
        if closest_distance <= FLEE_RADIUS:
            proximity = 1 - (closest_distance / FLEE_RADIUS)
            frame_scale = delta_time * BASELINE_FPS
            strength = closest_size_difference * proximity * FLEE_STRENGTH * frame_scale

            # TODO: Add the flee vector to self.vx and self.vy.
            self.vx += closest_flee_x * strength
            self.vy += closest_flee_y * strength

        # NOTE: clamp_speed() in update() will keep the velocity from getting too large.
        return

    def update(self, all_squares: list[SquareSnapshot], delta_time: float) -> None:
        """Update the square's position and bounce off walls."""
        self.apply_fleeing(all_squares, delta_time)
        self.apply_jitter(delta_time)
        self.clamp_speed()

        frame_scale = delta_time * BASELINE_FPS
        self.x += self.vx * frame_scale
        self.y += self.vy * frame_scale

        # Bounce off walls
        if self.x <= 0:
            self.x = 0
            if self.vx < 0:
                self.vx = -self.vx
        elif self.x + self.size >= WINDOW_WIDTH:
            self.x = WINDOW_WIDTH - self.size
            if self.vx > 0:
                self.vx = -self.vx

        if self.y <= 0:
            self.y = 0
            if self.vy < 0:
                self.vy = -self.vy
        elif self.y + self.size >= WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - self.size
            if self.vy > 0:
                self.vy = -self.vy

        # Keep square within bounds
        self.x = max(0, min(self.x, WINDOW_WIDTH - self.size))
        self.y = max(0, min(self.y, WINDOW_HEIGHT - self.size))

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the square on the given surface."""
        pygame.draw.rect(
            surface,
            self.color,
            (round(self.x), round(self.y), self.size, self.size),
        )


def main() -> None:
    """Main game loop."""
    sizes = [
        random.randint(MIN_SQUARE_SIZE, MAX_SQUARE_SIZE) for _ in range(NUM_SQUARES)
    ]
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
        delta_time = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Snapshot all squares before any updates so fleeing is not order-dependent.
        square_snapshots = [square.snapshot() for square in squares]

        for square in squares:
            square.update(square_snapshots, delta_time)

        screen.fill(WHITE)
        for square in squares:
            square.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()