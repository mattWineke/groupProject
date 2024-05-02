import pygame
import random

class PowerUp:
    # Constructor for PowerUp class
    def __init__(self, possibleXValues, y, width = 20, height = 20):
        self.possible_x_values = possibleXValues
        self.x = random.randint(possibleXValues[0], possibleXValues[1] - width)
        self.y = y - height # Subtract height to make sure it is shown on top of the surface it was placed on
        self.width = width
        self.height = height

        self.type = self.determineType()

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    # Method that gets called every frame
    def tick(self):
        self.updateHitbox()

    # Returns true if the power-up touches the target
    def collidedWith(self, target):
        return self.hitbox.colliderect(target.hitbox)

    # Method to apply a certain effect depending on the type of power-up 
    def applyEffect(self, player, settings):
        if self.type == 'slowMotion':
            settings["frame_rate"] = self.slowMotion(settings["frame_rate"])
        elif self.type == 'superJump':
            player.current_jumping_strength = self.superJump(player.current_jumping_strength)
        elif self.type == 'scoreBoost':
            settings["score"] = self.scoreBoost(settings["score"])

    # Method to update power-up's hitbox
    def updateHitbox(self):
        self.hitbox.x = self.x
        self.hitbox.y = self.y

    # Method to determine power-up's type
    def determineType(self):
        random_number = random.randint(1, 100)

        # Create a slow-motion power-up - 33% chance
        if random_number < 33:
            return "slowMotion"

        # Create a super-jump power-up - 33% chance
        elif random_number < 66:
            return "superJump"

        # Create a score boost power-up - 34% chance
        else:
            return "scoreBoost"
        
    def slowMotion(self, frame_rate):
        # Code to slow down movement
        return frame_rate
        
    def superJump(self, jumpStrength):
        # Code to change jump strength
        return jumpStrength
        
    def scoreBoost(self, score):
        # Code to increase score
        return score