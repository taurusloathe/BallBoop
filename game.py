import pygame
import tkinter as tk
from tkinter import messagebox
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("BallBoop")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)

# Paddle parameters
paddle_width, paddle_height = 100, 20
paddle_x = (width - paddle_width) // 2
paddle_y = height - 2 * paddle_height

# Ball parameters
ball_radius = 10
ball_x, ball_y = width // 2, height // 2
initial_ball_speed = 5
ball_speed_x, ball_speed_y = initial_ball_speed, -initial_ball_speed

# Brick parameters
brick_width, brick_height = 50, 20
num_bricks = 20

# Levels
current_level = 1
total_levels = 1  # We only have one level for simplicity

def initialize_bricks():
    return [
        pygame.Rect(x, y, brick_width, brick_height)
        for y in range(50, 50 + num_bricks * brick_height, brick_height)
        for x in range(0, width, width // (num_bricks // 2))
    ]

bricks = initialize_bricks()

# Score
score = 0

# Game state
game_paused = False

# Tkinter setup
root = tk.Tk()
root.withdraw()  # Hide the main Tkinter window

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_r and not game_paused:
                # Restart the game
                ball_x, ball_y = width // 2, height // 2
                ball_speed_x, ball_speed_y = initial_ball_speed, -initial_ball_speed
                bricks = initialize_bricks()
                current_level = 1
                score = 0
            elif event.key == K_p and not game_paused:
                # Pause the game
                game_paused = True
                pygame.time.delay(200)  # Add a slight delay to avoid instant response to key press
            elif event.key == K_r and game_paused:
                # Unpause the game
                game_paused = False
                pygame.time.delay(200)

    if not game_paused:
        # Move the paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= 5
        if keys[pygame.K_RIGHT] and paddle_x < width - paddle_width:
            paddle_x += 5

        # Move the ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Restart game if ball misses the paddle
        if ball_y > height:
            game_paused = True
            response = messagebox.askyesno("Game Over", "Would you like to restart?")
            if response:
                game_paused = False
                ball_x, ball_y = width // 2, height // 2
                ball_speed_x, ball_speed_y = initial_ball_speed, -initial_ball_speed
                bricks = initialize_bricks()
                current_level = 1
                score = 0
            else:
                pygame.quit()
                sys.exit()

        # Bounce off walls
        if ball_x <= 0 or ball_x >= width:
            ball_speed_x = -ball_speed_x
        if ball_y <= 0:
            ball_speed_y = -ball_speed_y

        # Bounce off paddle
        if (
            paddle_y <= ball_y <= paddle_y + paddle_height
            and paddle_x <= ball_x <= paddle_x + paddle_width
        ):
            ball_speed_y = -ball_speed_y

        # Check for collisions with bricks
        for brick in bricks:
            if brick.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, 2 * ball_radius, 2 * ball_radius)):
                bricks.remove(brick)
                score += 1
                ball_speed_y = -ball_speed_y  # Bounce the ball when hitting a brick

    # Draw everything
    screen.fill(black)
    pygame.draw.rect(screen, white, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, yellow, (int(ball_x), int(ball_y)), ball_radius)

    for brick in bricks:
        pygame.draw.rect(screen, green, brick)

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    # Display level
    level_text = font.render(f"Level: {current_level}", True, white)
    screen.blit(level_text, (width - 120, 10))

    # Update display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)

    # Check if the player has won the level
    if not bricks:
        current_level += 1
        ball_speed_x += 1  # Increase ball speed
        bricks = initialize_bricks()

        # Check if the player has won the game
        if current_level > total_levels:
            game_paused = True
            messagebox.showinfo("Congratulations", "You've won the game! Press 'R' to restart or close the window to exit.")
            response = messagebox.askyesno("Game Over", "Would you like to restart?")
            if response:
                game_paused = False
                ball_x, ball_y = width // 2, height // 2
                ball_speed_x, ball_speed_y = initial_ball_speed, -initial_ball_speed
                bricks = initialize_bricks()
                current_level = 1
                score = 0
            else:
                pygame.quit()
                sys.exit()

# Tkinter cleanup
root.destroy()
