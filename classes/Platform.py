import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Load platform sprites
platform_sprites = {
    "normal": pygame.image.load("normal_platform.png"),
    "moving": pygame.image.load("moving_platform.png"),
    "breakable": pygame.image.load("breakable_platform.png")
}

# Define the Platform class
class Platform:
    # Constructor for Platform class
    def __init__(self, sprites, x, y, current_score=0):           
        # Set platform type
        self.type = self.determine_platform_type()
        
        # Load sprites
        self.platform_sprite = sprites[self.type]

        # Initialize sprite rectangle
        self.sprite_rect = self.platform_sprite.get_rect(y=-500)  # -500 to make sure the platform appears out of the screen

        # Platform's dimensions
        self.width = self.sprite_rect.width
        self.height = self.sprite_rect.height
        
        # Platform's initial coordinates
        self.x = x
        self.y = y

        # Platform's state
        self.touched = False
        self.hasChangedScore = False
        self.hasEnemy = False
        self.hasPowerUp = False

        # Initialize platform's hitbox
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    # Method that gets called every frame
    def tick(self):
        self.update_hitbox()
        
        if self.type == "moving":
            self.move_platform()

        elif self.type == "breakable":
            self.check_if_platform_should_break()

    # Method to determine platform's type
    def determine_platform_type(self):
        random_number = random.randint(1, 100)

        # Create a normal platform: 60% chance
        if random_number < 60:
            return "normal"

        # Create a moving platform: 20% chance
        elif random_number < 80:
            return "moving"

        # Create a breakable platform: 20% chance
        else:
            return "breakable"
        
    # There is one in {argument} chances method returns true
    def one_in_x_chances(self, x):
        return random.randint(1, 100) <= 100 / x

    # Method to update platform's hitbox
    def update_hitbox(self):
        self.hitbox.x = self.x
        self.hitbox.y = self.y

    # Method that gets called every frame if it's a moving platform
    def move_platform(self):
        # Move the platform up and down in a loop
        if self.y <= -self.height:
            self.y = 600  # Reset position if platform goes above the screen
        else:
            self.y -= 1  # Move platform upwards

    # Method that gets called every frame if it's a breakable platform
    def check_if_platform_should_break(self):
        # self.touched is set to True when player jumps on it
        if self.touched:
            # Code to break platform
            self.platform_sprite = pygame.image.load("broken_platform.png")

# Main game loop
running = True
platforms = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Generate new platforms
    if len(platforms) < 10:
        platform = Platform(platform_sprites, random.randint(0, screen_width - 100), screen_height, current_score=0)
        platforms.append(platform)

    # Update platforms
    for platform in platforms:
        platform.tick()

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw platforms
    for platform in platforms:
        screen.blit(platform.platform_sprite, (platform.x, platform.y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
