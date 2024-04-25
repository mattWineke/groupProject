import pygame
import sys

from classes.Player import Player
from classes.Platform import Platform
from classes.Obstacle import Obstacle
from classes.PowerUp import PowerUp
        
pygame.init()          
surface = pygame.display.set_mode((400, 800))
pygame.display.set_caption("Pluto's Pursuit")
clock = pygame.time.Clock()

# Object instances
player = Player(50, 50)
platform = Platform(100, 50)

# Will be updated in the main loop, and attached to a label on the top left
score = None

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

        clock.tick(45)  # Set the frame rate to 45 FPS

    pygame.quit()  # Quit pygame properly
    sys.exit()  


if __name__ == "__main__":
    main()