import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400

# Load background image once (after pygame.init)
background = pygame.image.load("python_bg.jpg")  # replace with your image filename
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # scale to fit window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)

clock = pygame.time.Clock()
FPS = 10

BLOCK_SIZE = 20
snake_body = [[100, 50], [80, 50], [60, 50]]
direction = "RIGHT"

BUTTON_WIDTH = 160
BUTTON_HEIGHT = 48
BUTTON_COLOR = (50, 150, 50)
BUTTON_TEXT_COLOR = (255, 255, 255)

food_pos = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
            random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
food_spawn = True

score = 0
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"
            elif event.key == pygame.K_r and game_over:
                # Restart game on 'R' key
                snake_body = [[100, 50], [80, 50], [60, 50]]
                direction = "RIGHT"
                food_pos = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                            random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
                food_spawn = True
                score = 0
                game_over = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mx, my = event.pos
            btn_x = WIDTH // 2 - BUTTON_WIDTH // 2
            btn_y = HEIGHT // 2 + 40
            if btn_x <= mx <= btn_x + BUTTON_WIDTH and btn_y <= my <= btn_y + BUTTON_HEIGHT:
                # Restart when clickable button pressed
                snake_body = [[100, 50], [80, 50], [60, 50]]
                direction = "RIGHT"
                food_pos = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                            random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
                food_spawn = True
                score = 0
                game_over = False

    if not game_over:
        # Move snake head
        head_x, head_y = snake_body[0]
        if direction == "UP":
            head_y -= BLOCK_SIZE
        elif direction == "DOWN":
            head_y += BLOCK_SIZE
        elif direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif direction == "RIGHT":
            head_x += BLOCK_SIZE

        new_head = [head_x, head_y]
        snake_body.insert(0, new_head)

        # Check if snake ate food (using collision detection)
        snake_rect = pygame.Rect(new_head[0], new_head[1], BLOCK_SIZE, BLOCK_SIZE)
        food_rect = pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE)

        if snake_rect.colliderect(food_rect):
            score += 1
            food_spawn = False

        else:
            snake_body.pop()  # Remove tail

        # Spawn new food
        if not food_spawn:
            food_pos = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                        random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
            # Ensure food doesn't spawn on snake body
            while food_pos in snake_body:
                food_pos = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                            random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
            food_spawn = True

        # Check collisions
        # Wall collision
        if (head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT):
            game_over = True

        # Self collision
        for block in snake_body[1:]:
            if new_head == block:
                game_over = True

    # Drawing
    screen.blit(background, (0, 0))  # draw background image

    # Draw snake
    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # Draw food
    pygame.draw.rect(screen, ORANGE, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if game_over:
        game_over_text = font.render("GAME OVER! Press Q to Quit", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            running = False

        # Draw restart button
        btn_x = WIDTH // 2 - BUTTON_WIDTH // 2
        btn_y = HEIGHT // 2 + 40
        pygame.draw.rect(screen, BUTTON_COLOR, pygame.Rect(btn_x, btn_y, BUTTON_WIDTH, BUTTON_HEIGHT))
        btn_font = pygame.font.Font(None, 30)
        btn_text = btn_font.render("Restart (R)", True, BUTTON_TEXT_COLOR)
        text_rect = btn_text.get_rect(center=(btn_x + BUTTON_WIDTH // 2, btn_y + BUTTON_HEIGHT // 2))
        screen.blit(btn_text, text_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()