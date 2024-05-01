import random

class Platform:
    # Constructor for Platform class
    def __init__(self, x, y, width = 100, height = 15, color = "white"):           
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.type = self.determinePlatformType()
        self.broken = False

        self.hasObstacle = False
        self.hasPowerUp = False

        # Set an obstacle: 100% / 5 = 20% Chance
        if self.oneInXChances(5):
            self.hasObstacle = True

        # Set an power-up: (100% - 20%) / 8 = 10% Chance            
        elif self.oneInXChances(8):
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
        
    def oneInXChances(self, x):
        return random.randint(1, 100) <= 100 / x


    # Method that gets called every frame if it's a moving platform
    def movePlatform(self):
        pass # Should make the platform move either up AND down, or left and right in a loop

    # Method that gets called every frame if it's a breakable platform
    def checkIfPlatformShouldBreak(self):
        # self.broken is set to True when player jumps on it
        if self.broken:
            pass # Code to break platform

    # Since the collision functionality is already implemented, we don't need a function that returns the platform's information anymore.