import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 26)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (220, 0, 0)

snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"

score = 0
level = 1
speed = 8


def generate_food():
    # Generate food not on snake
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        if (x, y) not in snake:
            return x, y


food = generate_food()
running = True
game_over = False

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Change snake direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    if not game_over:
        head_x, head_y = snake[0]

        # Move head
        if direction == "UP":
            head_y -= CELL
        elif direction == "DOWN":
            head_y += CELL
        elif direction == "LEFT":
            head_x -= CELL
        elif direction == "RIGHT":
            head_x += CELL

        new_head = (head_x, head_y)

        # Wall collision
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            game_over = True

        # Self collision
        if new_head in snake:
            game_over = True

        snake.insert(0, new_head)

        # Food collision
        if new_head == food:
            score += 1
            food = generate_food()

            # Increase level every 4 foods
            if score % 4 == 0:
                level += 1
                speed += 2
        else:
            snake.pop()

    # Draw snake
    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], CELL, CELL))

    # Draw food
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL, CELL))

    # Show score and level
    text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

    if game_over:
        over_text = font.render("GAME OVER", True, RED)
        screen.blit(over_text, (WIDTH // 2 - 80, HEIGHT // 2))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()