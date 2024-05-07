#Display page for the game

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display dimensions
WIDTH, HEIGHT = 400, 600
WINDOW_SIZE = (WIDTH, HEIGHT)

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create a display surface
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pluto's Pursuit")

# Fonts
title_font = pygame.font.SysFont(None, 60)
button_font = pygame.font.SysFont(None, 30)

# Main loop
def main():
    clock = pygame.time.Clock()
    running = True

    play_button = pygame.Rect(300, 400, 200, 50)
    how_to_play_button = pygame.Rect(550, 400, 200, 50)

    drop_menu_open = False

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if play_button.collidepoint(event.pos):
                        print("Play button clicked")
                    elif how_to_play_button.collidepoint(event.pos):
                        drop_menu_open = not drop_menu_open

        # Clear the screen
        screen.fill(BLACK)

        # Draw objects
        # Draw buttons
        pygame.draw.rect(screen, GRAY, play_button)
        pygame.draw.rect(screen, GRAY, how_to_play_button)
        # Draw text on buttons
        draw_text("Play", button_font, BLACK, screen, play_button.x + 80, play_button.y + 15)
        draw_text("How to Play", button_font, BLACK, screen, how_to_play_button.x + 20, how_to_play_button.y + 15)

        # Draw title
        draw_text("Pluto's Pursuit", title_font, bLUE, screen, WIDTH//2, 100)

        # Draw platform
        pygame.draw.rect(screen, GRAY, (100, 300, 600, 20))

        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Cap the frame rate at 60 FPS

    pygame.quit()
    sys.exit()

background = pygame.image.load("images/background/space.png")  # Load your background image
screen.blit(background, (0, 0))  # Blit the background image to the screen
Character = pygame.image.load("images/character/L1Pluto.png")  #load the character image
Character = pygame.image.load("images/character/R1Pluto.png")
screen.blit(background, (0, 0))  # Blit the background image to the screen



 # Draw characters, obstacles, etc. 

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Run the main function
if __name__ == "__main__":
    main()
    

