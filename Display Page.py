#Display page for the game

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display dimensions
WIDTH, HEIGHT = 400, 600
WINDOW_SIZE = (WIDTH, HEIGHT)

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create a display surface
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pluto's Pursuit")

# Main loop
def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(WHITE)

        # Draw objects
        # Draw a background
        # background = pygame.image.load("background.png")  # Load your background image
        # screen.blit(background, (0, 0))  # Blit the background image to the screen

        # Draw characters, obstacles, etc.

        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Cap the frame rate at 60 FPS

    pygame.quit()
