import math
import pygame
import random
from dataclasses import dataclass

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600
MIN_SQUARE_SIZE: int = 20
MAX_SQUARE_SIZE: int = 70
MIN_SPEED: float = 1.5
MAX_SPEED: float = 7.0
NUM_SQUARES: int = 20
FPS: int = 60
JITTER_ENABLED: bool = True
FLEE_RADIUS: int = 150
FLEE_STRENGTH: float = 0.25
CHASE_RADIUS: int = 150
CHASE_STRENGTH: float = 0.25
BASELINE_FPS: float = 60.0
MIN_LIFESPAN: float = 30.0
MAX_LIFESPAN: float = 180.0

# Colors
WHITE: tuple[int, int, int] = (255, 255, 255)
BLACK: tuple[int, int, int] = (0, 0, 0)

# Create the display
screen: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Random Moving Squares")
clock: pygame.time.Clock = pygame.time.Clock()
font: pygame.font.Font = pygame.font.SysFont(None, 28)


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
        self.x: float = float(x)
        self.y: float = float(y)
        self.size: int = size
        self.age: float = 0.0
        self.lifespan: float = random.uniform(MIN_LIFESPAN, MAX_LIFESPAN)

        # Bigger squares get a lower speed cap so size and motion stay easy to compare.
        # Guard against divide-by-zero if the size range collapses to one value.
        if MAX_SQUARE_SIZE == MIN_SQUARE_SIZE:
            self.max_speed: float = MAX_SPEED
        else:
            size_ratio: float = (self.size - MIN_SQUARE_SIZE) / (
                MAX_SQUARE_SIZE - MIN_SQUARE_SIZE
            )
            self.max_speed: float = MAX_SPEED - size_ratio * (MAX_SPEED - MIN_SPEED)
            self.max_speed = min(self.max_speed, MAX_SPEED)
            self.max_speed = max(MIN_SPEED, self.max_speed)

        # Pick a random movement direction and a speed that does not exceed max_speed.
        angle: float = random.uniform(0, 2 * math.pi)
        speed: float = random.uniform(MIN_SPEED, self.max_speed)
        self.vx: float = math.cos(angle) * speed
        self.vy: float = math.sin(angle) * speed

        # Random color
        self.color: tuple[int, int, int] = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

    def snapshot(self) -> SquareSnapshot:
        """Capture the square state so all updates use the same frame data."""
        return SquareSnapshot(owner=self, x=self.x, y=self.y, size=self.size)

    def update_age(self, delta_time: float) -> None:
        """Increase this square's elapsed lifetime."""
        self.age += delta_time

    def is_dead(self) -> bool:
        """Return True when this square reaches the end of its lifespan."""
        return self.age >= self.lifespan

    def should_apply_jitter(self, delta_time: float) -> bool:
        """Decide whether this square should jitter on the current frame."""
        if delta_time <= 0:
            return False

        # Keep the original 10% chance at 60 FPS, but scale it by elapsed time.
        chance_per_second = 0.1 * BASELINE_FPS
        chance_this_frame = min(1.0, chance_per_second * delta_time)
        return random.random() < chance_this_frame

    def compute_jitter_rotation(self, delta_time: float) -> float:
        """Return a small random rotation angle in radians."""
        max_angle_degrees = 5.0 * delta_time * BASELINE_FPS
        return math.radians(random.uniform(-max_angle_degrees, max_angle_degrees))

    def rotate_velocity(self, angle_radians: float) -> None:
        """Rotate (vx, vy) by angle_radians while preserving speed."""
        cos_a = math.cos(angle_radians)
        sin_a = math.sin(angle_radians)

        new_vx = self.vx * cos_a - self.vy * sin_a
        new_vy = self.vx * sin_a + self.vy * cos_a

        self.vx = new_vx
        self.vy = new_vy

    def apply_jitter(self, delta_time: float) -> None:
        """Apply jitter as a small rotation of the speed vector."""
        if not JITTER_ENABLED:
            return

        if self.should_apply_jitter(delta_time):
            angle = self.compute_jitter_rotation(delta_time)
            self.rotate_velocity(angle)

    def clamp_speed(self) -> None:
        """Clamp total velocity magnitude so it does not exceed the speed cap."""
        speed = math.hypot(self.vx, self.vy)
        if speed > self.max_speed and speed > 0:
            scale = self.max_speed / speed
            self.vx *= scale
            self.vy *= scale

    def _random_unit_direction(self) -> tuple[float, float]:
        """Return a safe random unit vector for overlap cases."""
        direction_x: float = random.uniform(-1, 1)
        direction_y: float = random.uniform(-1, 1)
        length: float = math.hypot(direction_x, direction_y)

        while length < 0.0001:
            direction_x = random.uniform(-1, 1)
            direction_y = random.uniform(-1, 1)
            length = math.hypot(direction_x, direction_y)

        return direction_x / length, direction_y / length

    def _find_closest_target(
        self,
        all_squares: list[SquareSnapshot],
        radius: float,
        *,
        seek_larger: bool,
    ) -> tuple[float, float, float, float] | None:
        """Find the nearest relevant square and the direction to use for it."""
        center_x: float = self.x + self.size / 2
        center_y: float = self.y + self.size / 2

        closest_distance: float = radius + 1
        closest_direction_x: float = 0.0
        closest_direction_y: float = 0.0
        closest_size_difference: float = 0.0

        for other in all_squares:
            if other.owner is self:
                continue

            if seek_larger:
                if other.size <= self.size:
                    continue
                other_center_x: float = other.x + other.size / 2
                other_center_y: float = other.y + other.size / 2
                dx: float = center_x - other_center_x
                dy: float = center_y - other_center_y
                size_difference: float = other.size - self.size
            else:
                if other.size >= self.size:
                    continue
                other_center_x = other.x + other.size / 2
                other_center_y = other.y + other.size / 2
                dx = other_center_x - center_x
                dy = other_center_y - center_y
                size_difference = self.size - other.size

            distance: float = math.hypot(dx, dy)
            if distance > radius:
                continue

            if distance == 0:
                direction_x, direction_y = self._random_unit_direction()
            else:
                direction_x = dx / distance
                direction_y = dy / distance

            if distance < closest_distance:
                closest_distance = distance
                closest_direction_x = direction_x
                closest_direction_y = direction_y
                closest_size_difference = size_difference

        if closest_distance <= radius:
            return (
                closest_distance,
                closest_direction_x,
                closest_direction_y,
                closest_size_difference,
            )

        return None

    def apply_fleeing(self, all_squares: list[SquareSnapshot], delta_time: float) -> None:
        """Push this square away from nearby larger squares."""
        target = self._find_closest_target(all_squares, FLEE_RADIUS, seek_larger=True)
        if target is None:
            return

        closest_distance, flee_x, flee_y, closest_size_difference = target
        proximity: float = 1 - (closest_distance / FLEE_RADIUS)
        strength_per_second: float = closest_size_difference * proximity * FLEE_STRENGTH
        strength: float = strength_per_second * delta_time * BASELINE_FPS

        self.vx += flee_x * strength
        self.vy += flee_y * strength

    def apply_chasing(self, all_squares: list[SquareSnapshot], delta_time: float) -> None:
        """Move this square toward nearby smaller squares."""
        target = self._find_closest_target(all_squares, CHASE_RADIUS, seek_larger=False)
        if target is None:
            return

        closest_distance, chase_x, chase_y, closest_size_difference = target
        proximity: float = 1 - (closest_distance / CHASE_RADIUS)
        strength_per_second: float = closest_size_difference * proximity * CHASE_STRENGTH
        strength: float = strength_per_second * delta_time * BASELINE_FPS

        self.vx += chase_x * strength
        self.vy += chase_y * strength

    def update(self, all_squares: list[SquareSnapshot], delta_time: float) -> None:
        """Update the square's position and bounce off walls."""
        self.update_age(delta_time)
        self.apply_chasing(all_squares, delta_time)
        self.apply_fleeing(all_squares, delta_time)
        self.apply_jitter(delta_time)
        self.clamp_speed()

        # Move using real elapsed time instead of fixed per-frame movement.
        self.x += self.vx * delta_time * BASELINE_FPS
        self.y += self.vy * delta_time * BASELINE_FPS

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


def draw_fps(surface: pygame.Surface, clock: pygame.time.Clock) -> None:
    """Draw the current FPS in the top-left corner."""
    fps_text: pygame.Surface = font.render(f"FPS: {clock.get_fps():.1f}", True, BLACK)
    surface.blit(fps_text, (10, 10))


def handle_lifespan_rebirth(squares: list[Square]) -> None:
    """Remove dead squares and spawn replacements while maintaining total count."""
    death_counter: int = 0
    alive_squares: list[Square] = []

    for square in squares:
        if square.is_dead():
            death_counter += 1
        else:
            alive_squares.append(square)

    # Spawn replacement squares to maintain pool size
    for _ in range(death_counter):
        size: int = random.randint(MIN_SQUARE_SIZE, MAX_SQUARE_SIZE)
        new_square: Square = Square(
            x=random.randint(0, WINDOW_WIDTH - size),
            y=random.randint(0, WINDOW_HEIGHT - size),
            size=size,
        )
        alive_squares.append(new_square)

    squares[:] = alive_squares

def main() -> None:
    """Main game loop."""
    sizes: list[int] = [
        random.randint(MIN_SQUARE_SIZE, MAX_SQUARE_SIZE) for _ in range(NUM_SQUARES)
    ]
    squares: list[Square] = [
        Square(
            size=size,
            x=random.randint(0, WINDOW_WIDTH - size),
            y=random.randint(0, WINDOW_HEIGHT - size),
        )
        for size in sizes
    ]

    running: bool = True
    while running:
        delta_time: float = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Snapshot all squares before any updates so fleeing is not order-dependent.
        square_snapshots: list[SquareSnapshot] = [square.snapshot() for square in squares]

        for square in squares:
            square.update(square_snapshots, delta_time)

        handle_lifespan_rebirth(squares)

        screen.fill(WHITE)
        for square in squares:
            square.draw(screen)

        draw_fps(screen, clock)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()