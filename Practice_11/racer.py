import pygame
import random

pygame.init()

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Practice 11")

clock = pygame.time.Clock()

# Colors
GREEN = (40, 150, 40)
DARK_ROAD = (45, 45, 45)
ROAD_LINE = (230, 230, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
RED = (200, 0, 0)
BLUE = (20, 80, 220)
GRAY = (120, 120, 120)
LIGHT_BLUE = (120, 180, 255)

font = pygame.font.SysFont("Verdana", 22)

# Road
road_x = 90
road_width = 320
line_y = 0
line_speed = 8

# Player
player = pygame.Rect(220, 560, 50, 90)
player_speed = 6

# Enemy
enemy = pygame.Rect(random.randint(120, 340), -120, 55, 95)
enemy_speed = 5

# Coin
coin = pygame.Rect(random.randint(120, 360), -50, 28, 28)
coin_weight = random.choice([1, 2, 3])

coins = 0
overtaken = 0
N = 5


def draw_car(rect, color):
    """Draw realistic-looking car using simple shapes."""
    pygame.draw.rect(screen, color, rect, border_radius=10)

    # Windows
    pygame.draw.rect(screen, LIGHT_BLUE, (rect.x + 10, rect.y + 12, rect.w - 20, 22), border_radius=5)
    pygame.draw.rect(screen, LIGHT_BLUE, (rect.x + 10, rect.y + 50, rect.w - 20, 25), border_radius=5)

    # Wheels
    pygame.draw.rect(screen, BLACK, (rect.x - 6, rect.y + 15, 8, 22), border_radius=3)
    pygame.draw.rect(screen, BLACK, (rect.right - 2, rect.y + 15, 8, 22), border_radius=3)
    pygame.draw.rect(screen, BLACK, (rect.x - 6, rect.y + 58, 8, 22), border_radius=3)
    pygame.draw.rect(screen, BLACK, (rect.right - 2, rect.y + 58, 8, 22), border_radius=3)

    # Head lights
    pygame.draw.circle(screen, YELLOW, (rect.x + 12, rect.y + 4), 5)
    pygame.draw.circle(screen, YELLOW, (rect.right - 12, rect.y + 4), 5)


def draw_road():
    """Draw road, grass, lane lines."""
    global line_y

    # Grass
    screen.fill(GREEN)

    # Road
    pygame.draw.rect(screen, DARK_ROAD, (road_x, 0, road_width, HEIGHT))

    # Road borders
    pygame.draw.line(screen, WHITE, (road_x, 0), (road_x, HEIGHT), 5)
    pygame.draw.line(screen, WHITE, (road_x + road_width, 0), (road_x + road_width, HEIGHT), 5)

    # Moving lane lines
    for y in range(-80, HEIGHT, 120):
        pygame.draw.rect(screen, ROAD_LINE, (WIDTH // 2 - 5, y + line_y, 10, 70), border_radius=3)

    line_y += line_speed
    if line_y >= 120:
        line_y = 0


running = True

while running:
    draw_road()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.left > road_x + 10:
        player.x -= player_speed

    if keys[pygame.K_RIGHT] and player.right < road_x + road_width - 10:
        player.x += player_speed

    # Enemy movement
    enemy.y += enemy_speed

    # If enemy leaves screen, it means player overtook it
    if enemy.top > HEIGHT:
        overtaken += 1
        enemy.y = -120
        enemy.x = random.randint(120, 340)

    # Coin movement
    coin.y += 5

    if coin.top > HEIGHT:
        coin.y = -50
        coin.x = random.randint(120, 360)
        coin_weight = random.choice([1, 2, 3])

    # Collect coin
    if player.colliderect(coin):
        coins += coin_weight

        coin.y = -50
        coin.x = random.randint(120, 360)
        coin_weight = random.choice([1, 2, 3])

        # Increase enemy speed after N coins
        if coins % N == 0:
            enemy_speed += 1
            line_speed += 1

    # Collision with enemy
    if player.colliderect(enemy):
        running = False

    # Draw objects
    draw_car(player, BLUE)
    draw_car(enemy, RED)

    # Draw coin
    pygame.draw.circle(screen, YELLOW, coin.center, 15)
    pygame.draw.circle(screen, BLACK, coin.center, 15, 2)
    coin_text = font.render(str(coin_weight), True, BLACK)
    screen.blit(coin_text, (coin.x + 7, coin.y + 1))

    # UI panel
    pygame.draw.rect(screen, WHITE, (5, 5, 220, 105), border_radius=10)

    coins_text = font.render(f"Coins: {coins}", True, BLACK)
    speed_text = font.render(f"Speed: {enemy_speed}", True, BLACK)
    overtaken_text = font.render(f"Overtaken: {overtaken}", True, BLACK)

    screen.blit(coins_text, (15, 15))
    screen.blit(speed_text, (15, 45))
    screen.blit(overtaken_text, (15, 75))

    pygame.display.update()
    clock.tick(60)

pygame.quit()