import pygame
import sys

from classes.Player import Player
from classes.Platform import Platform
from classes.Enemy import Enemy
from classes.PowerUp import PowerUp
from classes.Database import Database
from classes.Button import Button

from animations.animateInAndOut import *

# Named variables
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 800
FRAME_RATE = 45

# Color RGB codes
LIGHT_GREEN = (100, 255, 100)
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pluto's Pursuit")
clock = pygame.time.Clock()

# Initialize Font
FONT_FAMILY = "calibri, helvetica, arial"
font_size = 25
font_margin = 20
game_font = pygame.font.SysFont(FONT_FAMILY, font_size, bold = True)

# Load images
load = pygame.image.load
backgroundPath = "images/background"
characterPath = "images/character"
platformPath = "images/platforms"
enemyPath = "images/enemy"
powerupPath = "images/powerups"

background_image = load(f"{backgroundPath}/space.png")
cloud_image = load(f"{backgroundPath}/clouds.png")
satellite_image = load(f"{characterPath}/plutos_satalite.png")
playerImages = {
    "right": [load(f"{characterPath}/R1Pluto.png"), load(f"{characterPath}/R2Pluto.png"), load(f"{characterPath}/R3Pluto.png"), load(f"{characterPath}/R4Pluto.png")],
    "left": [load(f"{characterPath}/L1Pluto.png"), load(f"{characterPath}/L2Pluto.png"), load(f"{characterPath}/L3Pluto.png"), load(f"{characterPath}/L4Pluto.png")],
    "idle": [load(f"{characterPath}/I1Pluto.png"), load(f"{characterPath}/I2Pluto.png"), load(f"{characterPath}/I3Pluto.png"), load(f"{characterPath}/I4Pluto.png")],
}
platformImage = load(f"{platformPath}/platform1.png")
enemyImages = {
    'left': load(f"{enemyPath}/SpacemiteL.png"),
    'right': load(f"{enemyPath}/SpacemiteR.png"),
    'idle': load(f"{enemyPath}/Space_Slime.png"),
}
powerupImages = {
    'invincibility': load(f"{powerupPath}/powerup1.png"),
    'double_points': load(f"{powerupPath}/powerup2.png"),
    'score_boost': load(f"{powerupPath}/powerup3.png"),
}

# Database instance
db = Database()

# Player instance
pluto = Player(playerImages)
PLUTO_PERSONAL_SPACE = 15 # Distance between the satellite/power-up cues and pluto's image

# Set window icon to one of pluto's images
pygame.display.set_icon(pluto.sprites_right[0])

# Dictionary to store dynamic variables
DYNAMIC = {
    "score": 0,
    "high_score": db.getHighScore(),
    "invincibility": {
        "active": False,
        "timer": 0
    },
    "double_points": {
        "active": False,
        "timer": 0
    },
    "score_boost": {
        "active": False,
        "timer": 0
    },
}

# Lists with game objects
PLATFORMS = []
ENEMIES = []
POWERUPS = []

# Flag to control game state
running = True

# Function with game's main logic
def main():
    global running
    running = True
    
    # Main loop
    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame()

        # Manage game objects
        createObjects()
        removeOffScreenObjects()

        # Manage power-up effects
        handlePowerups()

        # Update Player instance every frame
        pluto.tick(PLATFORMS)

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


        # Draw background
        background_y_position = -(background_image.get_rect().height - WINDOW_HEIGHT) * (1 - max(0, min(1, (pluto.camera_y_offset / (20 * WINDOW_HEIGHT)))))
        surface.blit(background_image, (0, background_y_position))

        # Draw clouds if needed
        if (pluto.camera_y_offset < WINDOW_HEIGHT):
            CLOUDS_POSITION = (0, WINDOW_HEIGHT - (cloud_image.get_rect().height - 50) + pluto.camera_y_offset)
            surface.blit(cloud_image, CLOUDS_POSITION)
        
        # Draw pluto's satellite
        SATELLITE_POSITION = (pluto.x - PLUTO_PERSONAL_SPACE, pluto.y - PLUTO_PERSONAL_SPACE + pluto.camera_y_offset)
        surface.blit(satellite_image, SATELLITE_POSITION)
            
        # Draw pluto
        surface.blit(pluto.current_sprites[int(pluto.current_frame)], pluto.sprite_rect)
        pluto.sprite_rect.update(pluto.x, pluto.y + pluto.camera_y_offset, pluto.width, pluto.height)

        # Draw platforms
        for platform in PLATFORMS:
            surface.blit(platform.platform_sprite, platform.sprite_rect)
            platform.sprite_rect.update(platform.x, platform.y + pluto.camera_y_offset, platform.width, platform.height)

            # Update Platform instance every frame
            platform.tick(pluto)

            # Increase score if the platform is touched for the first time
            if platform.touched and not platform.hasChangedScore:
                DYNAMIC["score"] += 2 if DYNAMIC["double_points"]["active"] else 1
                platform.hasChangedScore = True

        # Draw enemies
        for enemy in ENEMIES:
            surface.blit(enemy.current_sprite, enemy.sprite_rect)
            enemy.sprite_rect.update(enemy.x, enemy.y + pluto.camera_y_offset, enemy.width, enemy.height)

            # Update Enemy instance every frame
            enemy.tick(WINDOW_WIDTH, WINDOW_HEIGHT)

            # Handle enemy collision with pluto
            if enemy.collidedWith(pluto):
                if DYNAMIC["invincibility"]["active"]:
                    enemy.die(playerFeetCoordinates = (pluto.x + pluto.width / 2, pluto.y + pluto.height - 10))

                else:
                    pluto.die()

        # Draw power-ups
        for powerup in POWERUPS:
            surface.blit(powerup.powerup_sprite, powerup.sprite_rect)
            powerup.sprite_rect.update(powerup.x, powerup.y + pluto.camera_y_offset, powerup.width, powerup.height)

            # Update Power-Up instance every frame
            powerup.tick()

            # Handle power-up collision with pluto
            if powerup.collidedWith(pluto): 
                powerup.applyEffect(DYNAMIC, FRAME_RATE)

                # Move power-up out of the screen so it's deleted by removeOffScreenObjects function
                powerup.y = WINDOW_HEIGHT * 2


        # Draw active power-up's visual effect
        if DYNAMIC["invincibility"]["active"]:
            # Draw a force field around Pluto
            animateCircleInAndOut(surface, RGB_color = (0, 0, 255), center = pluto.sprite_rect.center, initial_radius = 0, max_radius = pluto.height, 
                               max_alpha = 40, total_duration = 3, time_left = DYNAMIC["invincibility"]["timer"] / FRAME_RATE, animation_duration = 0.2)
            
        if DYNAMIC["score_boost"]["active"]:
            # Draw "+5" next to Pluto
            animateTextInAndOut(surface, game_font, text = "+5", initial_size = 0, max_size = 30, color = "green",
                             center = (pluto.x + pluto.width + PLUTO_PERSONAL_SPACE, pluto.y + pluto.camera_y_offset), total_duration = 0.8,
                             time_left = DYNAMIC["score_boost"]["timer"] / FRAME_RATE, animation_duration = 0.2)
            
        elif DYNAMIC["double_points"]["active"]:
            # Draw "2x" next to Pluto
            animateTextInAndOut(surface, game_font, text = "2x", initial_size = 0, max_size = 30, color = "dodgerblue2",
                             center = (pluto.x + pluto.width + PLUTO_PERSONAL_SPACE, pluto.y + pluto.camera_y_offset), total_duration = 5,
                             time_left = DYNAMIC["double_points"]["timer"] / FRAME_RATE, animation_duration = 0.3)


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
        clock.tick(FRAME_RATE)

    # Display end screen
    displayEndScreen()


# Function to fill the PLATFORMS, ENEMIES and POWERUPS lists with respective instances
def createObjects():
    PLATFORM_GAP = 200
    PADDING = 20
    CAMERA_UPPER_BOUND = -pluto.camera_y_offset

    last_platform_y_position = PLATFORMS[-1].y if PLATFORMS else WINDOW_HEIGHT - PADDING
    
    # Create a new platform if no platforms have been created or if the last platform created is already on the screen
    if not PLATFORMS or last_platform_y_position > CAMERA_UPPER_BOUND:
        new_platform_y_position = last_platform_y_position - PLATFORM_GAP
        possible_x_values = [PADDING, WINDOW_WIDTH - PADDING]
        platform_instance = Platform(platformImage, possible_x_values, new_platform_y_position, currentScore = DYNAMIC["score"])

        PLATFORMS.append(platform_instance)

        # Add an enemy if needed
        if platform_instance.hasEnemy:
            possible_x_values = [platform_instance.x, platform_instance.x + platform_instance.width]
            y_position = platform_instance.y
            enemy_instance = Enemy(enemyImages, possible_x_values, y_position)
            
            ENEMIES.append(enemy_instance)

        # Add a power-up if needed
        elif platform_instance.hasPowerUp:
            possible_x_values = [platform_instance.x, platform_instance.x + platform_instance.width]
            y_position = platform_instance.y
            powerup_instance = PowerUp(powerupImages, possible_x_values, y_position)
            
            POWERUPS.append(powerup_instance)

# Function to remove the platforms that have gone off-screen
def removeOffScreenObjects():
    global PLATFORMS, ENEMIES, POWERUPS
    CAMERA_LOWER_BOUND = WINDOW_HEIGHT - pluto.camera_y_offset

    # Filter out the platforms, enemies, and power-ups whose y-coordinate is below the camera's lower bound
    PLATFORMS = [platform for platform in PLATFORMS if platform.y < CAMERA_LOWER_BOUND]
    ENEMIES = [enemy for enemy in ENEMIES if enemy.y < CAMERA_LOWER_BOUND]
    POWERUPS = [powerup for powerup in POWERUPS if powerup.y < CAMERA_LOWER_BOUND]

# Function to remove power-up effects
def handlePowerups():
    for powerup in DYNAMIC.values():
        if isinstance(powerup, dict):
            # Decrement the timer if necessary
            powerup['timer'] = max(0, powerup['timer'] - 1)
            # Set the active property based on the time left on the timer
            powerup['active'] = powerup['timer'] > 0

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


# Function to display the end screen
def displayEndScreen():
    global running
    
    # Change high score if necessary
    DYNAMIC["high_score"] = max(DYNAMIC["score"], DYNAMIC["high_score"])
    
    # Named variables
    GAP = 70
    CONTENT_Y_POSITION = WINDOW_HEIGHT // 2 - 25

    # Initiate score text
    score_text = f"Final Score: {DYNAMIC['score']}"
    score_font = pygame.font.SysFont(FONT_FAMILY, 37, bold = True)
    score_surface = score_font.render(score_text, True, WHITE)
    score_rect = score_surface.get_rect(center=(WINDOW_WIDTH // 2, CONTENT_Y_POSITION - GAP))

    # Button Instances
    play_again_button = Button(
            text="Play Again", callback=startGame,
            x=WINDOW_WIDTH // 4, y=CONTENT_Y_POSITION,
            shortcutKeys=[pygame.K_p, pygame.K_s, pygame.K_DOWN]
        )

    exit_button = Button(
            text="Exit Game", callback=exitGame,
            x=WINDOW_WIDTH // 4, y=CONTENT_Y_POSITION + GAP,
            shortcutKeys=[pygame.K_q, pygame.K_e, pygame.K_ESCAPE]
        )
    
    while not running:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame()

        # Draw background
        surface.blit(background_image, (0, 0))

        # Draw the score
        surface.blit(score_surface, score_rect)

        # Draw buttons
        play_again_button.draw(surface)
        exit_button.draw(surface)

        # Update the display
        pygame.display.flip()
        clock.tick(FRAME_RATE)

# Function to start a new game
def startGame():
    # Reset player instance
    global pluto
    pluto = Player(playerImages)
    
    # Reset dynamic variables
    DYNAMIC["score"] = 0
    DYNAMIC["invincibility"]["timer"] = 0
    DYNAMIC["double_points"]["timer"] = 0
    DYNAMIC["score_boost"]["timer"] = 0

    # Reset objects
    PLATFORMS.clear()
    ENEMIES.clear()
    POWERUPS.clear()

    # Call main function
    main()

# Function to exit the program
def exitGame():
    db.setHighScore(max(DYNAMIC["score"], DYNAMIC["high_score"]))
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    startGame()