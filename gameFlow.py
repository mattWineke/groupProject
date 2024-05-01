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

# Will be updated in the main loop and attached to a label on the top left
score = 0

# List with platform objects
PLATFORMS = []

def main():
    running = True
    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Manage platforms
        createPlatforms()
        removeOffScreenPlatforms()

        # Update Player instance every frame
        pluto.tick(surfaces = PLATFORMS)

        # Check if the game should finish
        if isGameOver(): running = False

        # Movement controls
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
        pygame.draw.circle(surface, "red", (pluto.x, pluto.y + pluto.camera_y_offset), SATELLITE_RADIUS)

        # Draw pluto
        surface.blit(pluto.current_sprites[int(pluto.current_frame)], pluto.sprite_rect)
        pluto.sprite_rect.update(pluto.x, pluto.y + pluto.camera_y_offset, pluto.width, pluto.height)

        # Draw platforms
        for platform in PLATFORMS:
            pygame.draw.rect(surface, platform.color, pygame.Rect(platform.x, platform.y + pluto.camera_y_offset, platform.width, platform.height))

            # Update Platform instance every frame
            platform.tick()


        # Update the display
        pygame.display.flip()

        # Set frame rate
        clock.tick(FRAME_RATE)

    # Exit game
    pygame.quit()
    sys.exit()  


# Function to fill the PLATFORMS list with platform instances
def createPlatforms():
    PLATFORM_GAP = 200
    PADDING = 20
    PLATFORM_WIDTH = 100
    CAMERA_UPPER_BOUND = -pluto.camera_y_offset

    last_platform_y_position = PLATFORMS[-1].y if PLATFORMS else WINDOW_HEIGHT - PADDING
    
    # Create a new platform if no platforms have been created or if the last platform created is already on the screen
    if not PLATFORMS or last_platform_y_position > CAMERA_UPPER_BOUND:
        new_platform_y_position = last_platform_y_position - PLATFORM_GAP 
        new_platform_x_position = random.randint(PADDING, WINDOW_WIDTH - PLATFORM_WIDTH - PADDING)
        PLATFORMS.append(Platform(new_platform_x_position, new_platform_y_position, PLATFORM_WIDTH))

# Function to remove the platforms that have gone off-screen
def removeOffScreenPlatforms():
    global PLATFORMS
    CAMERA_LOWER_BOUND = WINDOW_HEIGHT - pluto.camera_y_offset

    # Filter out the platforms whose y-coordinate is higher (lower on the screen) than the camera's lower bound
    PLATFORMS = [platform for platform in PLATFORMS if platform.y < CAMERA_LOWER_BOUND]

# Function to check if the player has lost
def isGameOver():
    player_rect = pygame.Rect(pluto.x, pluto.y, pluto.width, pluto.height)

    # A number that allows enough room below the screen so pluto can completely dissapear before touching the trigger
    GAME_OVER_Y_POSITION = WINDOW_HEIGHT + pluto.height * 1.5 - pluto.camera_y_offset
    game_over_rect = pygame.Rect(-WINDOW_WIDTH, GAME_OVER_Y_POSITION, WINDOW_WIDTH * 3, 1)

    if player_rect.colliderect(game_over_rect):
        return True
    else:
        return False
        
if __name__ == "__main__":
    main()