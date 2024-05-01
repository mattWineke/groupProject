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

# Won't be needed after objects get images
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
        
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

# Lists with game objects
PLATFORMS = []
OBSTACLES = []
POWERUPS = []

def main():
    # Flag to control game state
    running = True

    # Main loop
    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Manage game objects
        createObjects()
        removeOffScreenObjects()

        # Update Player instance every frame
        pluto.tick(surfaces = PLATFORMS)

        # Check if the player has fallen off the screen
        if playerFell(): running = False

        # Movement controls
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: 
            pluto.move(-pluto.speed)

            pluto.current_direction = "left"
            pluto.current_sprites = pluto.sprites_left # Make the current sprite list left

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            pluto.move(pluto.speed)

            pluto.current_direction = "right"
            pluto.current_sprites = pluto.sprites_right # Make the current sprite list right

        else:
            pluto.current_direction = "idle"
            pluto.current_sprites = pluto.sprites_idle # Fall back to idle sprite list unless keys are being pressed

        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
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

        # Draw obstacles
        for obstacle in OBSTACLES:
            pygame.draw.rect(surface, RED, pygame.Rect(obstacle.x, obstacle.y + pluto.camera_y_offset, obstacle.width, obstacle.height))

            # Update Obstacle instance every frame
            obstacle.tick()

            # Handle obstacle collision with pluto
            if obstacle.collidedWith(pluto): pluto.die()

        # Draw power-ups
        for powerup in POWERUPS:
            pygame.draw.rect(surface, GREEN, pygame.Rect(powerup.x, powerup.y + pluto.camera_y_offset, powerup.width, powerup.height))

            # Update Power-Up instance every frame
            powerup.tick()

            # Handle power-up collision with pluto
            if powerup.collidedWith(pluto): powerup.applyEffect(pluto, score)


        # Update the display
        pygame.display.flip()

        # Set frame rate
        clock.tick(FRAME_RATE)

    # Exit game
    pygame.quit()
    sys.exit()  


# Function to fill the PLATFORMS, OBSTACLES and POWERUPS lists with respective instances
def createObjects():
    PLATFORM_GAP = 200
    PADDING = 20
    PLATFORM_WIDTH = 120
    CAMERA_UPPER_BOUND = -pluto.camera_y_offset

    last_platform_y_position = PLATFORMS[-1].y if PLATFORMS else WINDOW_HEIGHT - PADDING
    
    # Create a new platform if no platforms have been created or if the last platform created is already on the screen
    if not PLATFORMS or last_platform_y_position > CAMERA_UPPER_BOUND:
        new_platform_y_position = last_platform_y_position - PLATFORM_GAP
        new_platform_x_position = random.randint(PADDING, WINDOW_WIDTH - PLATFORM_WIDTH - PADDING)
        platform_instance = Platform(new_platform_x_position, new_platform_y_position, PLATFORM_WIDTH)

        PLATFORMS.append(platform_instance)

        # Add an obstacle if needed
        if platform_instance.hasObstacle:
            possible_x_values = [platform_instance.x, platform_instance.x + platform_instance.width]
            y_position = platform_instance.y
            obstacle_instance = Obstacle(possible_x_values, y_position)
            
            OBSTACLES.append(obstacle_instance)

        # Add a power-up if needed
        elif platform_instance.hasPowerUp:
            possible_x_values = [platform_instance.x, platform_instance.x + platform_instance.width]
            y_position = platform_instance.y
            powerup_instance = PowerUp(possible_x_values, y_position)
            
            POWERUPS.append(powerup_instance)

# Function to remove the platforms that have gone off-screen
def removeOffScreenObjects():
    global PLATFORMS, OBSTACLES, POWERUPS
    CAMERA_LOWER_BOUND = WINDOW_HEIGHT - pluto.camera_y_offset

    # Filter out the platforms, obstacles and power-ups whose y-coordinate is below the camera's lower bound
    PLATFORMS = [platform for platform in PLATFORMS if platform.y < CAMERA_LOWER_BOUND]
    OBSTACLES = [obstacle for obstacle in OBSTACLES if obstacle.y < CAMERA_LOWER_BOUND]
    POWERUPS = [powerup for powerup in POWERUPS if powerup.y < CAMERA_LOWER_BOUND]


# Function to check if the player has lost
def playerFell():
    # A number that allows enough room below the screen so pluto can completely disappear before touching the trigger
    GAME_OVER_Y_POSITION = WINDOW_HEIGHT + pluto.height * 1.5 - pluto.camera_y_offset

    # An object placed just below the visible screen
    game_over_rect = pygame.Rect(-WINDOW_WIDTH, GAME_OVER_Y_POSITION, WINDOW_WIDTH * 3, 1)

    if pluto.hitbox.colliderect(game_over_rect):
        return True
    else:
        return False
    
if __name__ == "__main__":
    main()