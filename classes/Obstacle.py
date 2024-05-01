import pygame
import random

# Named Variables
HITBOX_SHRINK_FACTOR = 10  # Make the game somewhat forgiving

class Obstacle:
    # Constructor for Obstacle class
    def __init__(self, possibleXValues, y, width=20, height=20):
        self.possible_x_values = possibleXValues
        self.x = random.randint(possibleXValues[0], possibleXValues[1] - width)
        self.y = y - height  # Subtract height to make sure it is shown on top of the surface it was placed on
        self.width = width
        self.height = height

        self.initHitbox()

    # Initializes or updates the hitbox, keeping it centered within the obstacle
    def initHitbox(self):
        hitbox_width = self.width / HITBOX_SHRINK_FACTOR
        hitbox_height = self.height / HITBOX_SHRINK_FACTOR
        hitbox_x = self.x + (self.width - hitbox_width) / 2
        hitbox_y = self.y + (self.height - hitbox_height) / 2

        self.hitbox = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

    # Method that gets called every frame
    def tick(self):
        self.updateHitbox()

    # Returns true if the obstacle touches the target
    def collidedWith(self, target):
        return self.hitbox.colliderect(target.hitbox)
    
    # Method to update obstacle's hitbox, keeping it centered within the obstacle
    def updateHitbox(self):
        hitbox_x = self.x + (self.width - self.hitbox.width) / 2
        hitbox_y = self.y + (self.height - self.hitbox.height) / 2
        self.hitbox.update(hitbox_x, hitbox_y, self.hitbox.width, self.hitbox.height)
