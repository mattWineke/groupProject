import pygame
import random

class PowerUp:
    # Constructor for PowerUp class
    def __init__(self, possibleXValues, y, color = "green", width = 20, height = 20):
        # Power-up's initial coordinates
        self.possible_x_values = possibleXValues
        self.x = random.randint(possibleXValues[0], possibleXValues[1] - width)
        self.y = y - height # Subtract height to make sure it is shown on top of the surface it was placed on

        # Power-up's dimensions
        self.width = width
        self.height = height

        # Power-up's color
        self.color = color

        # Set power-up's type
        self.type = self.determineType()

        # Initialize power-up's hitbox
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    # Method that gets called every frame
    def tick(self):
        self.updateHitbox()

    # Returns true if the power-up touches the target
    def collidedWith(self, target):
        return self.hitbox.colliderect(target.hitbox)

    # Method to apply a certain effect depending on the type of power-up 
    def applyEffect(self, controls, frameRate):
        if self.type == 'invincibility':
            controls["invincibility"]["timer"] = frameRate * 3 # Make power-up last 3 seconds

        elif self.type == 'double_points':
            controls["double_points"]["timer"] = frameRate * 5 # Make power-up last 5 seconds

        elif self.type == 'score_boost':
            controls["score_boost"]["timer"] = frameRate * 0.8 # For animation purposes
            
            controls["score"] += 5

    # Method to update power-up's hitbox
    def updateHitbox(self):
        self.hitbox.x = self.x
        self.hitbox.y = self.y

    # Method to determine power-up's type
    def determineType(self):
        random_number = random.randint(1, 100)

        # Create an invincibility power-up - 33% chance
        if random_number < 33:
            self.color = "blue"
            return "invincibility"

        # Create a double-points power-up - 33% chance
        elif random_number < 66:
            self.color = "darkorchid2"
            return "double_points"

        # Create a score-boost power-up - 34% chance
        else:
            return "score_boost"