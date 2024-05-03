import pygame
import random

class Platform:
    # Constructor for Platform class
    def __init__(self, x, y, currentScore = 0):           
        # Load sprites
        platformPath = "images/platforms"
        self.platform_sprite = pygame.image.load(f"{platformPath}/platform1.png")

        # Platform's dimensions
        self.width = self.platform_sprite.get_rect().width  # Get the width from the sprite
        self.height = self.platform_sprite.get_rect().height  # Get the height from the sprite
        
        # Platform's initial coordinates
        self.x = x
        self.y = y

        # Set current sprite and initialize sprite rectangle
        self.sprite_rect = self.platform_sprite.get_rect(center=(self.x, self.y))

        # Set platform type
        self.type = self.determinePlatformType()

        # Platform's state
        self.touched = False
        self.hasChangedScore = False

        self.hasEnemy = False
        self.hasPowerUp = False

        # Place an enemy: Chances increase as score does - At 200 there is an enemy on (almost) every platform
        if self.oneInXChances(max(5 - currentScore / 50, 1.1)):
            self.hasEnemy = True

        # Place a power-up: Chances increase as score does - Enemies still have priority over power-ups    
        elif self.oneInXChances(max(5 - currentScore / 50, 1.5)):
            self.hasPowerUp = True

    # Method that gets called every frame
    def tick(self):
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


    # Method that gets called every frame if it's a moving platform
    def movePlatform(self):
        pass # Should make the platform move either up AND down, or left and right in a loop

    # Method that gets called every frame if it's a breakable platform
    def checkIfPlatformShouldBreak(self):
        # self.touched is set to True when player jumps on it
        if self.touched:
            pass # Code to break platform