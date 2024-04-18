# This program will made by my group whose names i cannot spell yet, because it's a lot of work
# The program will use pygame to create a platformer, incorperating loops, animation, iteration,
# math, functions, libraries, and more

import pygame
import random
import sys
import os


class Player:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = 10
        self.is_jumping = False
        self.jump_height = 50
        self.jump_count = 10

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_count = self.jump_height

    def update_jump(self):
        if self.is_jumping:
            if self.jump_count > 0:
                self.y -= 5  # Adjust to control the jump height
                self.jump_count -= 1
            elif self.y < 775:  # Check if circle is above the bottom of the screen
                self.y += 10  # Adjust to control the fall speed
            else:
                self.is_jumping = False
                self.jump_count = self.jump_height
                
pygame.init()          
surface = pygame.display.set_mode((400, 800))
pygame.display.set_caption("Pluto's Pursuit")
clock = pygame.time.Clock()

# Object instance
player = Player(50, 50, 25)

class Platform:
    def __init__(self, x, y):           
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 80, 10)
        self.color='green'
        self.type=random.randint(1,3) #will be able to this for a method that controls that type of platform it is
        self.visible=True  #Will be useful if the platform is one that breaks
        self.collision=True #same as the line above
    
    

platform = Platform(100, 50)

def loop(player):          #moves the object to the other side of the screen if they move too far
    if player.x <= -40:
        player.x = 418
    if player.x >= 420:
        player.x = -39

def movePlayer(player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-player.speed, 0)
    if keys[pygame.K_RIGHT]:
        player.move(player.speed, 0)
    if keys[pygame.K_UP]:
        player.y-=10  # Maybe freeze here
    if keys[pygame.K_DOWN]:
        player.move(0, player.speed)
    if keys[pygame.K_SPACE]:
        player.jump()
        print(player.x,"",player.y)

    # Allow movement during jump
    if player.is_jumping:  # Check if the player is currently jumping
        if keys[pygame.K_LEFT]:  # Allow left movement during jump
            player.move(-player.speed, 0)
        if keys[pygame.K_RIGHT]:  # Allow right movement during jump
            player.move(player.speed, 0)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Set running to False to exit the loop

        movePlayer(player)
        loop(player)
        player.update_jump()

        surface.fill((0, 0, 0))  # Clear the screen
        
        #pygame.draw.rect(surface,platform.x,platform.y,80,10)    #need to figure out argument format before this spawns correctly
        pygame.draw.circle(surface, "red", (player.x, player.y), player.radius)

        pygame.display.flip()  # Update the display

        clock.tick(60)  # Limit the frame rate to 60 FPS

    pygame.quit()  # Quit pygame properly
    sys.exit()  


main()
