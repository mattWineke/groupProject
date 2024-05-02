import pygame
import random

# Named Variables
HITBOX_SHRINK_FACTOR = 5  # Make the game somewhat forgiving

class Enemy:
    # Constructor for Enemy class
    def __init__(self, possibleXValues, y):
        # Load sprites
        enemyPath = "images/enemy"
        self.sprite_left = pygame.image.load(f"{enemyPath}/SpacemiteL.png")
        self.sprite_right = pygame.image.load(f"{enemyPath}/SpacemiteR.png")

        # Enemy's dimensions
        self.width = self.sprite_right.get_rect().width  # Get the width from the sprite
        self.height = self.sprite_right.get_rect().height  # Get the height from the sprite
        
        # Enemy's initial coordinates
        self.min_x_value = possibleXValues[0]
        self.max_x_value = possibleXValues[1] - self.width
        self.x = random.randint(self.min_x_value, self.max_x_value)
        self.y = y - self.height  # Adjust y to ensure it's shown on top of the surface it was placed on

        # Movement controls
        self.moving_enemy = self.oneInXChances(3) # ~33% chance
        self.speed = random.random() * 2
        self.direction = random.choice([-1, 1])  # 1 for right, -1 for left

        # Set current sprite and initialize sprite rectangle
        self.current_sprite = self.sprite_right if self.direction == 1 else self.sprite_left
        self.sprite_rect = self.current_sprite.get_rect(center=(self.x, self.y))

        # Initialize enemy's hitbox
        self.initHitbox()

    # Initializes enemy's hitbox
    def initHitbox(self):
        hitbox_width = self.width / HITBOX_SHRINK_FACTOR
        hitbox_height = self.height / HITBOX_SHRINK_FACTOR
        hitbox_x = self.x + (self.width - hitbox_width) / 2
        hitbox_y = self.y + (self.height - hitbox_height) / 2

        self.hitbox = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

    # Method that gets called every frame
    def tick(self):
        self.updateHitbox()
        if self.moving_enemy: self.move()

    # Move the enemy considering platform surface
    def move(self):
        self.x += self.speed * self.direction

        # If enemy has reached platform border
        if self.x <= self.min_x_value or self.x >= self.max_x_value:
            # Reverse direction
            self.direction *= -1

            # Update sprite
            self.current_sprite = self.sprite_left if self.direction == -1 else self.sprite_right

    # Returns true if the enemy touches the target
    def collidedWith(self, target):
        return self.hitbox.colliderect(target.hitbox)
    
    # Method to update ememy's hitbox, making sure it's centered
    def updateHitbox(self):
        hitbox_x = self.x + (self.width - self.hitbox.width) / 2
        hitbox_y = self.y + (self.height - self.hitbox.height) / 2
        self.hitbox.update(hitbox_x, hitbox_y, self.hitbox.width, self.hitbox.height)

    # There is one in {argument} chances method returns true
    def oneInXChances(self, x):
        return random.randint(1, 100) <= 100 / x