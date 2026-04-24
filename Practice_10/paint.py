import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

screen.fill(WHITE)

current_color = BLACK
tool = "pen"
drawing = False
start_pos = None
brush_size = 5

colors = [BLACK, RED, GREEN, BLUE, YELLOW]
color_buttons = []

for i, color in enumerate(colors):
    rect = pygame.Rect(10 + i * 50, 10, 40, 40)
    color_buttons.append((rect, color))

font = pygame.font.SysFont("Arial", 22)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard tool selection
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                tool = "pen"
            elif event.key == pygame.K_r:
                tool = "rectangle"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_e:
                tool = "eraser"
            elif event.key == pygame.K_SPACE:
                screen.fill(WHITE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = mouse_pos

            # Check color buttons
            for rect, color in color_buttons:
                if rect.collidepoint(mouse_pos):
                    current_color = color
                    drawing = False

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = mouse_pos

            # Draw rectangle
            if tool == "rectangle" and start_pos:
                x1, y1 = start_pos
                x2, y2 = end_pos
                rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(screen, current_color, rect, 3)

            # Draw circle
            elif tool == "circle" and start_pos:
                x1, y1 = start_pos
                x2, y2 = end_pos
                radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                pygame.draw.circle(screen, current_color, start_pos, radius, 3)

    # Pen and eraser drawing
    if drawing and pygame.mouse.get_pressed()[0]:
        if tool == "pen":
            pygame.draw.circle(screen, current_color, mouse_pos, brush_size)
        elif tool == "eraser":
            pygame.draw.circle(screen, WHITE, mouse_pos, 15)

    # Draw toolbar background
    pygame.draw.rect(screen, (230, 230, 230), (0, 0, WIDTH, 60))

    # Draw color buttons
    for rect, color in color_buttons:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    # Show selected tool
    text = font.render("P=Pen  R=Rectangle  C=Circle  E=Eraser  SPACE=Clear", True, BLACK)
    screen.blit(text, (270, 20))

    tool_text = font.render(f"Tool: {tool}", True, BLACK)
    screen.blit(tool_text, (10, 65))

    pygame.display.update()
    clock.tick(60)

pygame.quit()