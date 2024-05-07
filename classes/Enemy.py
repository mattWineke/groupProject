import pygame
import random

class Enemy:
    # Constructor for Enemy class
    def __init__(self, sprites, possibleXValues, y):
        self.is_alive = True
        
        # Movement controls
        self.moving_enemy = self.oneInXChances(3) # ~33% chance
        self.speed = random.random() * 2
        self.direction = random.choice([-1, 1])  # 1 for right, -1 for left
        
        # Load sprites
        self.sprite_left = sprites["left"]
        self.sprite_right = sprites["right"]

        # Set current sprite and initialize sprite rectangle
        self.current_sprite = self.sprite_right if self.direction == 1 else self.sprite_left
        self.sprite_rect = self.current_sprite.get_rect(y = -500) # -500 to make sure the enemy appears out of the screen

        # Enemy's dimensions
        self.width = self.sprite_rect.width
        self.height = self.sprite_rect.height
        
        # Enemy's initial coordinates
        self.min_x_value = possibleXValues[0]
        self.max_x_value = possibleXValues[1] - self.width
        self.x = random.randint(self.min_x_value, self.max_x_value)
        self.y = y - self.height  # Adjust y to ensure it's shown on top of the surface it was placed on

        # Initialize enemy's hitbox
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    # Method that gets called every frame
    def tick(self):
        self.updateHitbox()
        
        if not self.is_alive: self.die()
        elif self.moving_enemy: self.move()

    # Move the enemy considering platform surface
    def move(self):
        self.x += self.speed * self.direction

        # If enemy has reached platform border
        if self.x < self.min_x_value or self.x > self.max_x_value:
            # Reverse direction
            self.direction *= -1

            # Update sprite
            self.current_sprite = self.sprite_left if self.direction == -1 else self.sprite_right

    # Returns true if the enemy touches the target while being alive
    def collidedWith(self, target):
        return self.hitbox.colliderect(target.hitbox) and self.is_alive
    
    # Method to update enemy's hitbox
    def updateHitbox(self):
        self.hitbox.x = self.x
        self.hitbox.y = self.y

    # There is one in {argument} chances method returns true
    def oneInXChances(self, x):
        return random.randint(1, 100) <= 100 / x
    
    # Method that makes enemy fly away
    def die(self):
        if self.is_alive:
            self.is_alive = False
            self.current_sprite = pygame.transform.rotate(self.sprite_left, 35)

        # Check if the enemy is out of the screen
        if self.x + self.width > 0:
            self.x -= 15
            self.y -= 60

        else:
            # Move the enemy below the screen so it's deleted by removeOffScreenObjects function
            self.y = 2000