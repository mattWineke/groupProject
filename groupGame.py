#this program will made by my group who's names i cannot spell yet, because it's a lot of work
#the program will use pygame to create a platformer, incorperating loops, animation, iteration
#math, functions, libraries, and more

import pygame
import random
import sys
import os



class Player:
    def __init__(self, x, y):

        # The sprite animation frames
        self.sprites_right = [pygame.image.load("R1Pluto.png"), pygame.image.load("R2Pluto.png"),
                 pygame.image.load("R3Pluto.png"), pygame.image.load("R4Pluto.png") ]
        self.sprites_left = [pygame.image.load("L1Pluto.png"), pygame.image.load("L2Pluto.png"),
                pygame.image.load("L3Pluto.png"), pygame.image.load("L4Pluto.png")]
        self.sprites_idle = [pygame.image.load("I1Pluto.png"), pygame.image.load("I2Pluto.png"),
                        pygame.image.load("I3Pluto.png"), pygame.image.load("I4Pluto.png")]
        # PLayer current direction, for the sprite animations
        self.current_direction = "idle"
        self.current_sprites = self.sprites_idle # current sprite list
        self.current_frame = 0 # current index of the sprite frames
        
        self.sprite_rect = self.sprites_right[0].get_rect(center=[0,800])# Get sprite rectangle

        self.x = x
        self.y = y
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
            elif self.y < 775:  # Check if player is above the bottom of the screen
                self.y += 10  # Adjust to control the fall speed
            else:
                self.is_jumping = False
                self.jump_count = self.jump_height
                
pygame.init()          
surface = pygame.display.set_mode((400, 800))
pygame.display.set_caption("Pluto's Pursuit")
clock = pygame.time.Clock()

# Object instance
player = Player(50, 50)

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
    frame_rate = 10 #animation speed
    current_frame = 0
    clock = pygame.time.Clock()

    keys = pygame.key.get_pressed()

    player.current_direction = "idle"
    player.current_sprites = player.sprites_idle #fall back to idle sprite list unless keys are being pressed
    
    if keys[pygame.K_LEFT]: 
        player.current_direction = "left"
        player.current_sprites = player.sprites_left # make the current sprite list left
        current_frame += 0.2
        player.move(-player.speed, 0)

    if keys[pygame.K_RIGHT]:
        player.current_direction = "right"
        player.current_sprites = player.sprites_right # make the current sprite list right
        current_frame += 0.2
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

def animationLooping():
    
    player.current_frame += 0.2
    if player.current_frame >= len(player.current_sprites): 
        player.current_frame = 0
    if player.current_frame == 4:
        player.current_frame = 0



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
        
        animationLooping() 

        #pygame.draw.rect(surface,platform.x,platform.y,80,10)    #need to figure out argument format before this spawns correctly
        #pygame.draw.circle(surface, "red", (player.x, player.y), player.sprite_rect)
        surface.blit(player.current_sprites[int(player.current_frame)], (player.x, player.y))

        pygame.display.flip()  # Update the display

        clock.tick(30)  # Limit the frame rate to 30 FPS # I changed it from 60

    pygame.quit()  # Quit pygame properly
    sys.exit()  


main()
