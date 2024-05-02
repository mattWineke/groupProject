import random
import pygame

class Platform:
    # Constructor for Platform class
    def __init__(self, x, y, width = 100, height = 15, color = "black", currentScore = 0):    

        # Lists with Sprite animation frames
        load = pygame.image.load
        platformPath = "images/platforms"

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.platform_sprite = load(f"{platformPath}/platform1.png")
        
        self.sprite_rect = self.platform_sprite.get_rect(topleft=(344, 65))

        self.type = self.determinePlatformType()

        self.touched = False
        self.hasChangedScore = False

        self.hasEnemy = False
        self.hasPowerUp = False

        # Place an enemy: Chances increase as score does - At 200 there is an enemy on (almost) every platform
        if self.oneInXChances(max(5 - currentScore / 50, 1.1)):
            self.hasEnemy = True

        # Place a power-up: Chances increase as score does - Enemies still have priority over power-ups    
        elif self.oneInXChances(max(3 - currentScore / 100, 1)):
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

        # Create a normal platform: 60% chanceimport random
import pygame

class Platform:
    # Constructor for Platform class
    def __init__(self, x, y, width = 100, height = 15, color = "black", currentScore = 0):    

        # Lists with Sprite animation frames
        load = pygame.image.load
        platformPath = "images/platforms"

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.platform_sprite = load(f"{platformPath}/platform1.png")
        
        self.sprite_rect = self.platform_sprite.get_rect(topleft=(344, 65))

        self.type = self.determinePlatformType()

        self.touched = False
        self.hasChangedScore = False

        self.hasEnemy = False
        self.hasPowerUp = False

        # Place an enemy: Chances increase as score does - At 200 there is an enemy on (almost) every platform
        if self.oneInXChances(max(5 - currentScore / 50, 1.1)):
            self.hasEnemy = True

        # Place a power-up: Chances increase as score does - Enemies still have priority over power-ups    
        elif self.oneInXChances(max(3 - currentScore / 100, 1)):
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

    # Since the collision functionality is already implemented, we don't need a function that returns the platform's information anymore.
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

    # Since the collision functionality is already implemented, we don't need a function that returns the platform's information anymore.import random

class Platform:
    # Constructor for Platform class
    def __init__(self, x, y, width = 100, height = 15, color = "white", currentScore = 0):           
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.type = self.determinePlatformType()

        self.touched = False
        self.hasChangedScore = False

        self.hasEnemy = False
        self.hasPowerUp = False

        # Place an enemy: Chances increase as score does - At 200 there is an enemy on (almost) every platform
        if self.oneInXChances(max(5 - currentScore / 50, 1.1)):
            self.hasEnemy = True

        # Place a power-up: Chances increase as score does - Enemies still have priority over power-ups    
        elif self.oneInXChances(max(3 - currentScore / 100, 1)):
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

    # Since the collision functionality is already implemented, we don't need a function that returns the platform's information anymore.
