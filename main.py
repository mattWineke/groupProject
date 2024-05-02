import pygame
import sys
import random

from classes.Player import Player
from classes.Platform import Platform
from classes.Enemy import Enemy
from classes.PowerUp import PowerUp
from classes.Database import Database
        
# Named variables
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 800

# Most colors won't be needed after objects get images
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (100, 255, 100)
WHITE = (255, 255, 255)
        
# Initialize Pygame
pygame.init() 
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pluto's Pursuit")
clock = pygame.time.Clock()

# Initialize Font
pygame.font.init()
font_size = 30
font_margin = 20
game_font = pygame.font.Font(None, font_size)

# Load background image
backgroundPath = "images/background" 
bg = pygame.image.load(f"{backgroundPath}/space.png")

# Database instance
db = Database()

# Player instance
pluto = Player()

# Set window icon to one of pluto's images
pygame.display.set_icon(pluto.sprites_right[0])

# Dictionary to store dynamic variables
DYNAMIC = {
    "frame_rate": 45,
    "score": 0,
    "high_score": db.get_high_score()
}

# Lists with game objects
PLATFORMS = []
ENEMIES = []
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
        surface.blit(bg, (0, 0))
        
        # Draw pluto's satellite
        SATELLITE_RADIUS = 10
        SATELLITE_COLOR = (min(DYNAMIC["score"] * 255 / 200, 255), max(255 - DYNAMIC["score"] * 255 / 200, 0), 0) # (Red, Green, Blue) - 255: Max Intensity - 200: Score satellite is totally red
        pygame.draw.circle(surface, SATELLITE_COLOR, (pluto.x, pluto.y + pluto.camera_y_offset), SATELLITE_RADIUS)

        # Draw pluto
        surface.blit(pluto.current_sprites[int(pluto.current_frame)], pluto.sprite_rect)
        pluto.sprite_rect.update(pluto.x, pluto.y + pluto.camera_y_offset, pluto.width, pluto.height)

        # Draw platforms
        for platform in PLATFORMS:
            surface.blit(platform.platform_sprite, platform.sprite_rect)
            platform.sprite_rect.update(platform.x, platform.y + pluto.camera_y_offset, platform.width, platform.height)

            # Update Platform instance every frame
            platform.tick()

            # Increase score if the platform is touched for the first time
            if platform.touched and not platform.hasChangedScore: 
                DYNAMIC["score"] += 1
                platform.hasChangedScore = True

        # Draw enemies
        for enemy in ENEMIES:
            surface.blit(enemy.current_sprite, enemy.sprite_rect)
            enemy.sprite_rect.update(enemy.x, enemy.y + pluto.camera_y_offset, enemy.width, enemy.height)

            # Update Enemy instance every frame
            enemy.tick()

            # Handle enemy collision with pluto
            if enemy.collidedWith(pluto): pluto.die()

        # Draw power-ups
        for powerup in POWERUPS:
            pygame.draw.rect(surface, GREEN, pygame.Rect(powerup.x, powerup.y + pluto.camera_y_offset, powerup.width, powerup.height))

            # Update Power-Up instance every frame
            powerup.tick()

            # Handle power-up collision with pluto
            if powerup.collidedWith(pluto): 
                powerup.applyEffect(pluto, DYNAMIC)

                # Move power-up out of the screen so it's deleted by removeOffScreenObjects function
                powerup.y = WINDOW_HEIGHT * 2


        # Display current score
        score_text = f"Score: {DYNAMIC['score']}"
        score_surface = game_font.render(score_text, True, WHITE)
        score_coordinates = (font_margin, font_margin)
        surface.blit(score_surface, score_coordinates)

        # Display high score
        high_score_text = f"High Score: {max(DYNAMIC['high_score'], DYNAMIC['score'])}"
        high_score_color = WHITE if DYNAMIC["score"] <= DYNAMIC["high_score"] else LIGHT_GREEN # Change text color if new high score is being set
        high_score_surface = game_font.render(high_score_text, True, high_score_color)
        high_score_text_width = high_score_surface.get_width()
        high_score_coordinates = (WINDOW_WIDTH - high_score_text_width - font_margin, font_margin)
        surface.blit(high_score_surface, high_score_coordinates)
        


        # Update the display
        pygame.display.flip()

        # Set frame rate
        clock.tick(DYNAMIC["frame_rate"])

    # If there's a new high score, save it
    if DYNAMIC["score"] > DYNAMIC["high_score"]: 
        db.set_high_score(DYNAMIC["score"])

    # Exit game
    pygame.quit()
    sys.exit()


# Function to fill the PLATFORMS, ENEMIES and POWERUPS lists with respective instances
def createObjects():
    PLATFORM_GAP = 200
    PADDING = 20
    PLATFORM_WIDTH = 132
    CAMERA_UPPER_BOUND = -pluto.camera_y_offset

    last_platform_y_position = PLATFORMS[-1].y if PLATFORMS else WINDOW_HEIGHT - PADDING
    
    # Create a new platform if no platforms have been created or if the last platform created is already on the screen
    if not PLATFORMS or last_platform_y_position > CAMERA_UPPER_BOUND:
        new_platform_y_position = last_platform_y_position - PLATFORM_GAP
        new_platform_x_position = random.randint(PADDING, WINDOW_WIDTH - PLATFORM_WIDTH - PADDING)
        platform_instance = Platform(new_platform_x_position, new_platform_y_position, currentScore = DYNAMIC["score"])

        PLATFORMS.append(platform_instance)

        # Add an enemy if needed
        if platform_instance.hasEnemy:
            possible_x_values = [platform_instance.x, platform_instance.x + platform_instance.width]
            y_position = platform_instance.y
            enemy_instance = Enemy(possible_x_values, y_position)
            
            ENEMIES.append(enemy_instance)

        # Add a power-up if needed
        elif platform_instance.hasPowerUp:
            possible_x_values = [platform_instance.x, platform_instance.x + platform_instance.width]
            y_position = platform_instance.y
            powerup_instance = PowerUp(possible_x_values, y_position)
            
            POWERUPS.append(powerup_instance)

# Function to remove the platforms that have gone off-screen
def removeOffScreenObjects():
    global PLATFORMS, ENEMIES, POWERUPS
    CAMERA_LOWER_BOUND = WINDOW_HEIGHT - pluto.camera_y_offset

    # Filter out the platforms, enemies, and power-ups whose y-coordinate is below the camera's lower bound
    PLATFORMS = [platform for platform in PLATFORMS if platform.y < CAMERA_LOWER_BOUND]
    ENEMIES = [enemy for enemy in ENEMIES if enemy.y < CAMERA_LOWER_BOUND]
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