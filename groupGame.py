import pygame
import random
import sys
import os
import GameObjectClasses as game

        
pygame.init()          
surface = pygame.display.set_mode((400, 800))
pygame.display.set_caption("Pluto's Pursuit")
clock = pygame.time.Clock()

# Object instance
player = game.Player(50, 50)
platform = game.Platform(100, 50)


score=None  #will be updated in the main loop, and attached to a label on the top left



def main():

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Set running to False to exit the loop

        player.movePlayer()
        player.loop()
        player.update_jump()

        surface.fill((0, 0, 0))  # Clear the screen
        
        player.animationLooping() 

        pygame.draw.circle(surface, "red", (player.x, player.y), player.radius)
        pygame.draw.rect(surface,'green',platform.rect)
        surface.blit(player.current_sprites[int(player.current_frame)], (player.x, player.y))

        pygame.display.flip()  # Update the display

        clock.tick(45)  # Limit the frame rate to 30 FPS # I changed it from 60

    pygame.quit()  # Quit pygame properly
    sys.exit()  


main()

