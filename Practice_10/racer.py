import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (220, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 215, 0)
BLACK = (0, 0, 0)

player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 90, 50, 80)
enemy = pygame.Rect(random.randint(50, WIDTH - 100), -100, 50, 80)
coin = pygame.Rect(random.randint(40, WIDTH - 40), -200, 25, 25)

player_speed = 6
enemy_speed = 6
coin_speed = 5
score = 0

running = True
while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed

    # Move enemy car
    enemy.y += enemy_speed
    if enemy.top > HEIGHT:
        enemy.y = -100
        enemy.x = random.randint(50, WIDTH - 100)

    # Move coin
    coin.y += coin_speed
    if coin.top > HEIGHT:
        coin.y = -200
        coin.x = random.randint(40, WIDTH - 40)

    # Collision with coin
    if player.colliderect(coin):
        score += 1
        coin.y = -200
        coin.x = random.randint(40, WIDTH - 40)

    # Collision with enemy
    if player.colliderect(enemy):
        running = False

    # Draw road lines
    for y in range(0, HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, y, 10, 40))

    # Draw objects
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, RED, enemy)
    pygame.draw.ellipse(screen, YELLOW, coin)

    # Show score in top right corner
    score_text = font.render(f"Coins: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 140, 20))

    pygame.display.update()
    clock.tick(60)

pygame.quit()