import pygame
import sys
import random

from classes.Player import Player
from classes.Platform import Platform
from classes.Obstacle import Obstacle
from classes.PowerUp import PowerUp
        
# Named variables
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 800
FRAME_RATE = 45

BLACK = (0, 0, 0)
        
# Initialize Pygame
pygame.init()    
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pluto's Pursuit")
clock = pygame.time.Clock()

# Player Object instance
pluto = Player()

# Set window icon to one of pluto's images
pygame.display.set_icon(pluto.sprites_right[0])

# Will be updated in the main loop, and attached to a label on the top left
score = 0

# List with platform objects
PLATFORMS = []

def createPlatforms():
    PLATFORM_GAP = 180
    PADDING = 20
    PLATFORM_WIDTH = 120

    last_platform_y_position = PLATFORMS[-1].y if PLATFORMS else WINDOW_HEIGHT - PADDING
    
    if not PLATFORMS or last_platform_y_position > 100:
        new_platform_y_position = last_platform_y_position - PLATFORM_GAP 
        new_platform_x_position = random.randint(PADDING, WINDOW_WIDTH - PLATFORM_WIDTH - PADDING)
        PLATFORMS.append(Platform(new_platform_x_position, new_platform_y_position, PLATFORM_WIDTH))


def main():
    running = True
    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Use createPlatforms function's algorithm to create a group of platforms
        createPlatforms()

        # Update Player instance every frame
        pluto.tick(surfaces = PLATFORMS)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]: 
            pluto.move(-pluto.speed)
            
            pluto.current_direction = "left"
            pluto.current_sprites = pluto.sprites_left # Make the current sprite list left

        elif keys[pygame.K_RIGHT]:
            pluto.move(pluto.speed)

            pluto.current_direction = "right"
            pluto.current_sprites = pluto.sprites_right # Make the current sprite list right

        else:
            pluto.current_direction = "idle"
            pluto.current_sprites = pluto.sprites_idle # Fall back to idle sprite list unless keys are being pressed

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            pluto.jump()

        # Print pluto's info when pressing p
        if keys[pygame.K_p]:
            print(pluto)


        # Draw background
        surface.fill(BLACK)
        
        # Draw pluto's satellite
        SATELLITE_RADIUS = 10
        pygame.draw.circle(surface, "red", (pluto.x, pluto.y), SATELLITE_RADIUS)

        # Draw pluto
        surface.blit(pluto.current_sprites[int(pluto.current_frame)], pluto.sprite_rect)
        pluto.sprite_rect.update(pluto.x, pluto.y, pluto.width, pluto.height)

        # Draw platforms
        for platform in PLATFORMS:
            pygame.draw.rect(surface, platform.color, pygame.Rect(platform.x, platform.y, platform.width, platform.height))

            # Update Platform instance every frame
            platform.tick()


        # Update the display
        pygame.display.flip()

        # Set frame rate
        clock.tick(FRAME_RATE)

    # Exit game
    pygame.quit()
    sys.exit()  

if __name__ == "__main__":
    main()