import pygame
import random

class Platform:
    # Constructor for Platform class
    def __init__(self, sprites, x, y, currentScore = 0):           
        # Set platform type
        self.type = self.determinePlatformType()
        
        # Load sprites
        self.platform_sprite = sprites[self.type]

        # Initialize sprite rectangle
        self.sprite_rect = self.platform_sprite.get_rect(y = -500) # -500 to make sure the platform appears out of the screen

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

        # Place an enemy: Chances increase as score does - At 200 there is an enemy on (almost) every platform
        if self.oneInXChances(max(4 - currentScore / (200 / 3), 1.2)):
            self.hasEnemy = True

        # Place a power-up: Chances increase as score does - Enemies still have priority over power-ups    
        elif self.oneInXChances(max(5 - currentScore / (200 / 4), 1.2)):
            self.hasPowerUp = True

        # Initialize platform's hitbox
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    # Method that gets called every frame
    def tick(self):
        self.updateHitbox()
        
        if self.type == "moving":
            self.movePlatform()

        elif self.type == "breakable":
            self.checkIfPlatformShouldBreak()

    # Method to determine platform's type
    def determinePlatformType(self):
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
    def oneInXChances(self, x):
        return random.randint(1, 100) <= 100 / x

    # Method to update platform's hitbox
    def updateHitbox(self):
        self.hitbox.x = self.x
        self.hitbox.y = self.y

    # Method that gets called every frame if it's a moving platform
    def movePlatform(self):
        pass # Should make the platform move either up AND down, or left and right in a loop

    # Method that gets called every frame if it's a breakable platform
    def checkIfPlatformShouldBreak(self):
        # self.touched is set to True when player jumps on it
        if self.touched:
            pass # Code to break platform