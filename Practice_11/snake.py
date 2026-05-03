import pygame
import random

pygame.init()

WIDTH, HEIGHT = 640, 480
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Practice 11")

clock = pygame.time.Clock()

# Colors
DARK_GREEN = (35, 95, 45)
LIGHT_GREEN = (45, 115, 55)
SNAKE_GREEN = (0, 180, 80)
SNAKE_DARK = (0, 120, 55)
RED = (220, 40, 40)
YELLOW = (255, 220, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Verdana", 22)

snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"

score = 0
speed = 10

food_lifetime = 4000  # 4 seconds


def generate_food():
    """Generate food with random position and weight."""
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(40, HEIGHT, CELL)

        if (x, y) not in snake:
            return (x, y), random.choice([1, 2, 3])


food, food_weight = generate_food()
food_spawn_time = pygame.time.get_ticks()


def draw_background():
    """Draw grass-like checkered background."""
    for x in range(0, WIDTH, CELL):
        for y in range(40, HEIGHT, CELL):
            color = DARK_GREEN if (x // CELL + y // CELL) % 2 == 0 else LIGHT_GREEN
            pygame.draw.rect(screen, color, (x, y, CELL, CELL))


def draw_snake():
    """Draw snake with rounded body and eyes."""
    for i, block in enumerate(snake):
        x, y = block

        color = SNAKE_GREEN if i == 0 else SNAKE_DARK
        pygame.draw.rect(screen, color, (x, y, CELL, CELL), border_radius=7)

        # Snake head eyes
        if i == 0:
            if direction == "RIGHT":
                pygame.draw.circle(screen, WHITE, (x + 14, y + 5), 3)
                pygame.draw.circle(screen, WHITE, (x + 14, y + 15), 3)
            elif direction == "LEFT":
                pygame.draw.circle(screen, WHITE, (x + 6, y + 5), 3)
                pygame.draw.circle(screen, WHITE, (x + 6, y + 15), 3)
            elif direction == "UP":
                pygame.draw.circle(screen, WHITE, (x + 5, y + 6), 3)
                pygame.draw.circle(screen, WHITE, (x + 15, y + 6), 3)
            elif direction == "DOWN":
                pygame.draw.circle(screen, WHITE, (x + 5, y + 14), 3)
                pygame.draw.circle(screen, WHITE, (x + 15, y + 14), 3)


def draw_food():
    """Draw apple-like food with weight."""
    x, y = food

    # Apple body
    pygame.draw.circle(screen, RED, (x + CELL // 2, y + CELL // 2), 9)

    # Apple shine
    pygame.draw.circle(screen, WHITE, (x + 7, y + 7), 3)

    # Leaf
    pygame.draw.ellipse(screen, LIGHT_GREEN, (x + 11, y - 2, 9, 6))

    # Weight text
    text = font.render(str(food_weight), True, YELLOW)
    screen.blit(text, (x + 23, y - 4))


running = True

while running:
    screen.fill(BLACK)
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    x, y = snake[0]

    if direction == "UP":
        y -= CELL
    elif direction == "DOWN":
        y += CELL
    elif direction == "LEFT":
        x -= CELL
    elif direction == "RIGHT":
        x += CELL

    new_head = (x, y)

    # Border collision
    if x < 0 or x >= WIDTH or y < 40 or y >= HEIGHT:
        running = False

    # Self collision
    if new_head in snake:
        running = False

    snake.insert(0, new_head)

    # Eat food
    if new_head == food:
        score += food_weight
        food, food_weight = generate_food()
        food_spawn_time = pygame.time.get_ticks()
    else:
        snake.pop()

    # Timer for disappearing food
    current_time = pygame.time.get_ticks()
    time_left = max(0, food_lifetime - (current_time - food_spawn_time))

    if time_left <= 0:
        food, food_weight = generate_food()
        food_spawn_time = pygame.time.get_ticks()

    draw_food()
    draw_snake()

    # Top UI bar
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 40))

    score_text = font.render(f"Score: {score}", True, WHITE)
    weight_text = font.render(f"Food weight: {food_weight}", True, WHITE)
    timer_text = font.render(f"Timer: {time_left // 1000 + 1}", True, WHITE)

    screen.blit(score_text, (10, 7))
    screen.blit(weight_text, (170, 7))
    screen.blit(timer_text, (410, 7))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()