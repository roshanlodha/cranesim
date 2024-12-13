import pygame
import math
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crane Simulator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Crane base properties
base_x = WIDTH // 2
base_y = HEIGHT - 50
base_width = 100
base_height = 20

# Crane arm properties
arm_length = 250
arm_angle = 0  # in degrees
arm_speed = 1  # degrees per frame

# Hook properties
hook_radius = 10
hook_x = base_x
hook_y = base_y - arm_length

# Movement flags
arm_rotating_left = False
arm_rotating_right = False
hook_moving_up = False
hook_moving_down = False
box_rotating_right = False
box_rotating_left = False
holding_container = False

# Hook limits
max_hook_length = arm_length + 450
min_hook_length = 50
current_hook_length = arm_length

# health and score tracking
total_health = 1
score = 0

# Initialize new container and box

def generate_container_and_box():
    global container_width, container_height, container_x, container_y, container_angle
    global box_width, box_height, box_x, box_y, box_angle

    container_width = random.randint(40, 60)
    container_height = random.randint(40, 60)
    container_x = random.randint(100, WIDTH - 100)
    container_y = random.randint(100, HEIGHT - 200)
    container_angle = random.randint(0, 360)

    box_width = container_width
    box_height = container_height
    box_x = random.randint(100, WIDTH - 100)
    box_y = random.randint(100, HEIGHT - 200)
    box_angle = random.randint(0, 360)

# Generate first container and box
generate_container_and_box()

# End game button properties
button_width, button_height = 100, 50
button_x, button_y = WIDTH - button_width - 10, HEIGHT - button_height - 10
button_color = (255, 100, 100)
button_text_color = BLACK

# Game loop
running = True
game_over = False

while running:
    screen.fill(WHITE)

    if game_over:
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))

        restart_font = pygame.font.Font(None, 36)
        restart_text = restart_font.render("Press R to Restart", True, BLACK)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game
                    total_health = 1
                    score = 0
                    game_over = False
                    generate_container_and_box()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                arm_rotating_right = True
            if event.key == pygame.K_RIGHT:
                arm_rotating_left = True
            if event.key == pygame.K_UP:
                hook_moving_down = True
            if event.key == pygame.K_DOWN:
                hook_moving_up = True
            if event.key == pygame.K_SPACE:
                holding_container = not holding_container
            if holding_container:
                if event.key == pygame.K_a:
                    box_rotating_left = True
                if event.key == pygame.K_d:
                    box_rotating_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                arm_rotating_right = False
            if event.key == pygame.K_RIGHT:
                arm_rotating_left = False
            if event.key == pygame.K_UP:
                hook_moving_down = False
            if event.key == pygame.K_DOWN:
                hook_moving_up = False
            if holding_container:
                if event.key == pygame.K_a:
                    box_rotating_left = False
                if event.key == pygame.K_d:
                    box_rotating_right = False

    # Rotate arm
    if arm_rotating_left:
        arm_angle -= arm_speed
    if arm_rotating_right:
        arm_angle += arm_speed

    if box_rotating_left:
        container_angle += 2
    if box_rotating_right:
        container_angle -= 2

    # Move hook
    if hook_moving_up and current_hook_length > min_hook_length:
        current_hook_length -= 2
    if hook_moving_down and current_hook_length < max_hook_length:
        current_hook_length += 2

    # Update hook position
    hook_x = base_x + math.cos(math.radians(arm_angle)) * current_hook_length
    hook_y = base_y - math.sin(math.radians(arm_angle)) * current_hook_length

    # Pickup or hold container
    if holding_container:
        container_x = hook_x - container_width // 2
        container_y = hook_y - container_height // 2

    # Check for container drop
    if not holding_container:
        container_rect = pygame.Rect(container_x, container_y, container_width, container_height)
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        if container_rect.colliderect(box_rect):
            overlap_width = min(container_x + container_width, box_x + box_width) - max(container_x, box_x)
            overlap_height = min(container_y + container_height, box_y + box_height) - max(container_y, box_y)
            if overlap_width > 0 and overlap_height > 0:
                current_health = round((overlap_width * overlap_height) / (container_width * container_height), 4)
                total_health *= current_health
                score += 1
                generate_container_and_box()

    # Game Over Condition
    if total_health < 0.01:
        game_over = True
    
    # Draw crane base
    pygame.draw.rect(screen, GRAY, (base_x - base_width // 2, base_y, base_width, base_height))

    # Draw crane arm
    arm_end_x = base_x + math.cos(math.radians(arm_angle)) * arm_length
    arm_end_y = base_y - math.sin(math.radians(arm_angle)) * arm_length
    pygame.draw.line(screen, BLACK, (base_x, base_y), (arm_end_x, arm_end_y), 5)

    # Draw hook
    pygame.draw.line(screen, BLACK, (arm_end_x, arm_end_y), (hook_x, hook_y), 2)
    pygame.draw.circle(screen, RED, (int(hook_x), int(hook_y)), hook_radius)

    # Draw container
    container_rect_surface = pygame.Surface((container_width, container_height), pygame.SRCALPHA)
    pygame.draw.rect(container_rect_surface, GREEN, (0, 0, container_width, container_height))
    rotated_container = pygame.transform.rotate(container_rect_surface, container_angle)
    screen.blit(rotated_container, rotated_container.get_rect(center=(container_x, container_y)))

    # Draw target box
    box_rect_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    pygame.draw.rect(box_rect_surface, BLUE, (0, 0, box_width, box_height), 2)
    rotated_box = pygame.transform.rotate(box_rect_surface, box_angle)
    screen.blit(rotated_box, rotated_box.get_rect(center=(box_x, box_y)))

    # Draw health
    font = pygame.font.Font(None, 36)
    health_percentage = int(round(total_health, 2) * 100)
    health_text = font.render(f"Total Health: {health_percentage}%", True, BLACK)
    screen.blit(health_text, (10, 10))

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 50))

    # # Draw end game button
    # pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
    # button_font = pygame.font.Font(None, 24)
    # button_text = button_font.render("End Game", True, button_text_color)
    # screen.blit(button_text, (button_x + 10, button_y + 15))

    # Draw instructions
    instruction_font = pygame.font.Font(None, 24)
    instructions = [
        "Arrow keys: Move crane arm and hook",
        "Space: Pick up/drop container",
        "A/D: Rotate box (must be picked up)"
    ]
    for i, text in enumerate(instructions):
        instruction_text = instruction_font.render(text, True, BLACK)
        screen.blit(instruction_text, (10, HEIGHT - (len(instructions) - i) * 20))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
