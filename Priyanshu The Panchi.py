import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 30
GRAVITY = 1
BIRD_SIZE = 60
PIPE_WIDTH = 50
PIPE_HEIGHT = 300
PIPE_GAP = 220
GROUND_HEIGHT = 30
BACKGROUND_SCROLL_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Priyanshu The Panchi")

# Load images
background_image = pygame.image.load("background.png")
ground_image = pygame.image.load("ground.png")
bird_image = pygame.image.load("bird.png")
pipe_image = pygame.image.load("pipe.png")

# Resize images
bird_image = pygame.transform.scale(bird_image, (BIRD_SIZE, BIRD_SIZE))
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, PIPE_HEIGHT))

# Clock to control the frame rate
clock = pygame.time.Clock()

# Game variables
bird_x = WIDTH // 8
bird_y = HEIGHT // 4
bird_velocity = 0
pipes = []
score = 0
background_scroll = 0

# Fonts
font = pygame.font.Font(None, 36)

def draw_bird(x, y):
    screen.blit(bird_image, (x, y))

def draw_pipe(x, gap_top, gap_bottom):
    screen.blit(pipe_image, (x, gap_top - PIPE_HEIGHT))
    screen.blit(pipe_image, (x, gap_bottom))

def draw_ground(scroll):
    screen.blit(ground_image, (scroll, HEIGHT - GROUND_HEIGHT))

def draw_background(scroll):
    screen.blit(background_image, (scroll, 0))

def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over():
    game_over_text = font.render("Har Gaya Bhai", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    display_score(score)
    pygame.display.flip()
    pygame.time.wait(2000)
    reset_game()

def reset_game():
    global bird_y, bird_velocity, pipes, score, background_scroll
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    background_scroll = 0

# Function to generate pipes
def generate_pipe():
    gap_top = random.randint(50, HEIGHT - 50 - PIPE_GAP)
    gap_bottom = gap_top + PIPE_GAP
    return {"x": WIDTH, "gap_top": gap_top, "gap_bottom": gap_bottom}

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bird_y + BIRD_SIZE > HEIGHT:
                    reset_game()
                else:
                    bird_velocity = -15

    # Move bird
    bird_y += bird_velocity
    bird_velocity += GRAVITY

    # Generate pipes
    if len(pipes) == 0 or pipes[-1]["x"] < WIDTH - WIDTH // 2:
        pipes.append(generate_pipe())

    # Move pipes
    for pipe in pipes:
        pipe["x"] -= 5

        # Check for collisions with pipes
        if bird_x < pipe["x"] + PIPE_WIDTH and bird_x + BIRD_SIZE > pipe["x"]:
            if bird_y < pipe["gap_top"] or bird_y + BIRD_SIZE > pipe["gap_bottom"]:
                game_over()

        # Check for passing pipes
        if pipe["x"] + PIPE_WIDTH < bird_x:
            score += 1

    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if pipe["x"] + PIPE_WIDTH > 0]

    # Check for collisions with the ground and ceiling
    if bird_y < 0:
        bird_y = 0
        bird_velocity = 0
    elif bird_y + BIRD_SIZE > HEIGHT - GROUND_HEIGHT:
        game_over()

    # Clear the screen
    draw_background(background_scroll)
    
    # Draw pipes
    for pipe in pipes:
        draw_pipe(pipe["x"], pipe["gap_top"], pipe["gap_bottom"])

    # Draw bird
    draw_bird(bird_x, bird_y)

    # Draw ground
    draw_ground(background_scroll)
    background_scroll -= BACKGROUND_SCROLL_SPEED

    # Display score
    display_score(score)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
