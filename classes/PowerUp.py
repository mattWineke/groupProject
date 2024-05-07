import pygame
import random

class PowerUp:
    # Constructor for PowerUp class
    def __init__(self, possibleXValues, y):
        # Set power-up's type
        self.type = self.determineType()
        
        # Power-ups' images
        powerupPath = "images/powerups"
        powerupImages = {
            'invincibility': f"{powerupPath}/powerup1.png",
            'double_points': f"{powerupPath}/powerup2.png",
            'score_boost': f"{powerupPath}/powerup3.png"
        }

        # Load appropriate sprite
        self.powerup_sprite = pygame.image.load(powerupImages[self.type])

        # Powerup's dimensions
        self.width = self.powerup_sprite.get_rect().width
        self.height = self.powerup_sprite.get_rect().height

        # Power-up's coordinates
        self.possible_x_values = possibleXValues
        self.x = random.randint(possibleXValues[0], possibleXValues[1] - self.width)
        self.y = y - self.height # Subtract height to make sure it is shown on top of the surface it was placed on

        # Initialize sprite rectangle
        self.sprite_rect = self.powerup_sprite.get_rect(center=(self.x, self.y))

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
            return "invincibility"

        # Create a double-points power-up - 33% chance
        elif random_number < 66:
            return "double_points"

        # Create a score-boost power-up - 34% chance
        else:            
            return "score_boost"