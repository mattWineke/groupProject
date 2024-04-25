#This is a game project Pseudocode for our platfrom jumping game.

# Import required libraries
import pygame
import random
import sys

# Define Player class
class Player:
    # Initialize player attributes
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = 10
        self.is_jumping = False
        self.jump_height = 100
        self.jump_count = 10
    
    # Method to move player
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    # Method to initiate player jump
    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_count = self.jump_height
    
    # Method to update player's jump motion
    def update_jump(self):
        if self.is_jumping:
            if self.jump_count >= -self.jump_height: 
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = self.jump_height

# Initialize pygame
pygame.init()
surface = pygame.display.set_mode((400, 800))
pygame.display.set_caption("Not Doodle Jump")
clock = pygame.time.Clock()

# Define Platform class
class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 80, 10)
    
    # Method to draw platform
    def draw(self, surface):
        pygame.draw.rect(surface, "green", self.rect)

# Create player and platform objects
player = Player(50, 50, 25)
platform = Platform(200, 300)

# Define loop to handle player movement across screen boundaries
def loop(player):
    if player.x <= -40:
        player.x = 418
    if player.x >= 420:
        player.x = -39

# Function to handle player movement
def movePlayer(player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-player.speed, 0)
    if keys[pygame.K_RIGHT]:
        player.move(player.speed, 0)
    if keys[pygame.K_DOWN]:
        player.move(0, player.speed)
    if keys[pygame.K_SPACE]:
        player.jump()
    if player.is_jumping:
        if keys[pygame.K_LEFT]:
            player.move(-player.speed, 0)
        if keys[pygame.K_RIGHT]:
            player.move(player.speed, 0)

# Main function to run the game
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        movePlayer(player)
        loop(player)
        player.update_jump()
        
        surface.fill((0, 0, 0))
        pygame.draw.circle(surface, "red", (player.x, player.y), player.radius)
        platform.draw(surface)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

# Call the main function to start the game
main()
