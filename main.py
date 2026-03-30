import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SQUARE_SIZE = 40
NUM_SQUARES = 10
FPS = 60

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
        # Random velocity for each direction (-5 to 5 pixels per frame)
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        # Random color
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    
    def update(self) -> None:
        """Update the square's position and bounce off walls."""
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
    # Create squares at random positions
    squares = [
        Square(
            random.randint(0, WINDOW_WIDTH - SQUARE_SIZE),
            random.randint(0, WINDOW_HEIGHT - SQUARE_SIZE),
            SQUARE_SIZE
        )
        for _ in range(NUM_SQUARES)
    ]
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update squares
        for square in squares:
            square.update()
        
        # Draw everything
        screen.fill(WHITE)
        for square in squares:
            square.draw(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()


if __name__ == "__main__":
    main()
