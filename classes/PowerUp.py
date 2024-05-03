import pygame
import random

class PowerUp:
    # Constructor for PowerUp class
    def __init__(self, possibleXValues, y, color = "green", width = 20, height = 20):
        # Power-up's initial coordinates
        self.possible_x_values = possibleXValues
        self.x = random.randint(possibleXValues[0], possibleXValues[1] - width)
        self.y = y - height # Subtract height to make sure it is shown on top of the surface it was placed on

        # load sprite images
        powerupPath = "images/powerups"
        self.powerup1 = pygame.image.load(f"{powerupPath}/powerup1.png")
        self.powerup2 = pygame.image.load(f"{powerupPath}/powerup2.png")
        self.powerup3 = pygame.image.load(f"{powerupPath}/powerup3.png")

         # powerup's dimensions
        self.powerup1_width = self.powerup1.get_rect().width  # Get the width from the sprite
        self.powerup1_height = self.powerup1.get_rect().height  # Get the height from the sprite

        self.powerup2_width = self.powerup2.get_rect().width  # Get the width from the sprite
        self.powerup2_height = self.powerup2.get_rect().height  # Get the height from the sprite

        self.powerup3_width = self.powerup3.get_rect().width  # Get the width from the sprite
        self.powerup3_height = self.powerup3.get_rect().height  # Get the height from the spri

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
            # Set width for current sprite
            self.width = self.powerup1_width
            self.height = self.powerup1_height
            # powerupsprite set to the current power up sprite
            self.powerupsprite = self.powerup1
            # power up rect
            self.sprite_rect = self.powerupsprite.get_rect(center=(self.x, self.y))
            return "invincibility"

        # Create a double-points power-up - 33% chance
        elif random_number < 66:
            self.color = "darkorchid2"
            # Set width for current sprite
            self.width = self.powerup2_width
            self.height = self.powerup2_height
            # powerupsprite set to the current power up sprite
            self.powerupsprite = self.powerup2
            # power up rect
            self.sprite_rect = self.powerupsprite.get_rect(center=(self.x, self.y))
            return "double_points"

        # Create a score-boost power-up - 34% chance
        else:
            # Set width for current sprite
            self.width = self.powerup3_width
            self.height = self.powerup3_height
            # powerupsprite set to the current power up sprite
            self.powerupsprite = self.powerup3
            # power up rect
            self.sprite_rect = self.powerupsprite.get_rect(center=(self.x, self.y))
            
            return "score_boost"
