import pygame
import math

pygame.init()

WIDTH, HEIGHT = 900, 650
MENU_HEIGHT = 95

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Practice 11 ")

clock = pygame.time.Clock()

WHITE = (245, 245, 245)
BLACK = (0, 0, 0)
GRAY = (215, 215, 215)
DARK_GRAY = (60, 60, 60)
RED = (230, 40, 40)
GREEN = (40, 170, 70)
BLUE = (40, 90, 230)
YELLOW = (240, 200, 20)

screen.fill(WHITE)

font = pygame.font.SysFont("Verdana", 15)
current_color = BLACK
current_shape = "line"
eraser_size = 25
start_pos = None


def draw_menu():
    """Draw menu inside the screen."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, MENU_HEIGHT))
    pygame.draw.line(screen, DARK_GRAY, (0, MENU_HEIGHT), (WIDTH, MENU_HEIGHT), 3)

    text1 = "0 Line | 1 Rectangle | 2 Circle | 3 Square | 4 Right Triangle"
    text2 = "5 Equilateral Triangle | 6 Rhombus | E Eraser"
    text3 = "Colors: R Red | G Green | B Blue | Y Yellow | K Black | C Clear"

    screen.blit(font.render(text1, True, BLACK), (15, 10))
    screen.blit(font.render(text2, True, BLACK), (15, 37))
    screen.blit(font.render(text3, True, BLACK), (15, 64))

    pygame.draw.rect(screen, WHITE, (650, 15, 220, 55), border_radius=8)
    screen.blit(font.render(f"Tool: {current_shape}", True, BLACK), (660, 22))
    screen.blit(font.render("Color:", True, BLACK), (660, 48))
    pygame.draw.circle(screen, current_color, (740, 56), 10)
    pygame.draw.circle(screen, BLACK, (740, 56), 10, 2)


def draw_shape(start, end):
    """Draw selected shape."""
    x1, y1 = start
    x2, y2 = end

    width = x2 - x1
    height = y2 - y1

    if current_shape == "rectangle":
        rect = pygame.Rect(x1, y1, width, height)
        rect.normalize()
        pygame.draw.rect(screen, current_color, rect, 3)

    elif current_shape == "circle":
        radius = int(math.sqrt(width ** 2 + height ** 2))
        pygame.draw.circle(screen, current_color, (x1, y1), radius, 3)

    elif current_shape == "square":
        size = min(abs(width), abs(height))
        if width < 0:
            x1 -= size
        if height < 0:
            y1 -= size
        pygame.draw.rect(screen, current_color, (x1, y1, size, size), 3)

    elif current_shape == "right_triangle":
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(screen, current_color, points, 3)

    elif current_shape == "equilateral_triangle":
        size = abs(width)
        direction = 1 if width >= 0 else -1

        p1 = (x1, y1)
        p2 = (x1 + direction * size, y1)
        p3 = (x1 + direction * size // 2, y1 - int(size * math.sqrt(3) / 2))

        pygame.draw.polygon(screen, current_color, [p1, p2, p3], 3)

    elif current_shape == "rhombus":
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        points = [
            (center_x, y1),
            (x2, center_y),
            (center_x, y2),
            (x1, center_y)
        ]

        pygame.draw.polygon(screen, current_color, points, 3)


running = True

while running:
    draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Choose tool or color
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                current_shape = "line"
            elif event.key == pygame.K_1:
                current_shape = "rectangle"
            elif event.key == pygame.K_2:
                current_shape = "circle"
            elif event.key == pygame.K_3:
                current_shape = "square"
            elif event.key == pygame.K_4:
                current_shape = "right_triangle"
            elif event.key == pygame.K_5:
                current_shape = "equilateral_triangle"
            elif event.key == pygame.K_6:
                current_shape = "rhombus"
            elif event.key == pygame.K_e:
                current_shape = "eraser"

            elif event.key == pygame.K_r:
                current_color = RED
            elif event.key == pygame.K_g:
                current_color = GREEN
            elif event.key == pygame.K_b:
                current_color = BLUE
            elif event.key == pygame.K_y:
                current_color = YELLOW
            elif event.key == pygame.K_k:
                current_color = BLACK

            elif event.key == pygame.K_c:
                screen.fill(WHITE)

        # Start drawing
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] > MENU_HEIGHT:
                start_pos = event.pos

        # Draw with eraser while mouse moves
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0] and current_shape == "line":
                x, y = event.pos
                if y > MENU_HEIGHT:
                    pygame.draw.circle(screen, current_color, (x, y), 4)
            if pygame.mouse.get_pressed()[0] and current_shape == "eraser":
                x, y = event.pos
                if y > MENU_HEIGHT:
                    pygame.draw.circle(screen, WHITE, (x, y), eraser_size)

        # Finish drawing shape
        if event.type == pygame.MOUSEBUTTONUP and start_pos is not None:
            if current_shape != "eraser":
                end_pos = event.pos

                if end_pos[1] < MENU_HEIGHT:
                    end_pos = (end_pos[0], MENU_HEIGHT)

                draw_shape(start_pos, end_pos)

            start_pos = None

    pygame.display.update()
    clock.tick(60)

pygame.quit()