import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 75, 20
ROWS, COLS = 5, 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Game clock
clock = pygame.time.Clock()

# Paddle class
class Paddle:
    def __init__(self):
        self.x = WIDTH // 2 - PADDLE_WIDTH // 2
        self.y = HEIGHT - PADDLE_HEIGHT - 20
        self.speed = 7

    def move(self, dx):
        self.x += dx
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH - PADDLE_WIDTH:
            self.x = WIDTH - PADDLE_WIDTH

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Ball class
class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = random.choice([-5, 5])
        self.dy = -5
        self.radius = BALL_RADIUS

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.dx = -self.dx

        if self.y - self.radius < 0:
            self.dy = -self.dy

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

# Brick class
class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = random.choice([GREEN, BLUE, RED])

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Create the game objects
paddle = Paddle()
ball = Ball()

# Create the bricks
bricks = []
for i in range(ROWS):
    for j in range(COLS):
        bricks.append(Brick(j * (BRICK_WIDTH + 10) + 50, i * (BRICK_HEIGHT + 10) + 50))

# Game loop
running = True
score = 0

while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement (left and right)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move(-paddle.speed)
    if keys[pygame.K_RIGHT]:
        paddle.move(paddle.speed)

    # Ball movement
    ball.move()

    # Check collision with paddle
    if (paddle.y < ball.y + ball.radius < paddle.y + PADDLE_HEIGHT) and (paddle.x < ball.x < paddle.x + PADDLE_WIDTH):
        ball.dy = -ball.dy

    # Check collision with bricks
    for brick in bricks[:]:
        if (brick.y < ball.y + ball.radius < brick.y + brick.height) and (brick.x < ball.x < brick.x + brick.width):
            ball.dy = -ball.dy
            bricks.remove(brick)  # Remove the brick
            score += 10  # Increase the score

    # Check if ball falls below the paddle
    if ball.y > HEIGHT:
        print(f"Game Over! Final Score: {score}")
        running = False

    # Draw the game elements
    paddle.draw()
    ball.draw()
    for brick in bricks:
        brick.draw()

    # Display the score
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Check if all bricks are destroyed
    if not bricks:
        print(f"You Win! Final Score: {score}")
        running = False

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
