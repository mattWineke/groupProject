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
player = Player()
platform = Platform(100, 50)

# Will be updated in the main loop, and attached to a label on the top left
score = None

def main():
    running = True
    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update Player instance
        player.tick()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]: 
            player.current_direction = "left"
            player.current_sprites = player.sprites_left # make the current sprite list left
            
            player.move(-player.speed)

        elif keys[pygame.K_RIGHT]:
            player.current_direction = "right"
            player.current_sprites = player.sprites_right # make the current sprite list right

            player.move(player.speed)

        else:
            player.current_direction = "idle"
            player.current_sprites = player.sprites_idle #fall back to idle sprite list unless keys are being pressed

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            player.jump()

        # Print player object info when pressing p
        if keys[pygame.K_p]:
            print(player)

        surface.fill((0, 0, 0))
        
        pygame.draw.circle(surface, "red", (player.x, player.y), player.radius)
        pygame.draw.rect(surface,'green',platform.rect)
        surface.blit(player.current_sprites[int(player.current_frame)], (player.x, player.y))

        pygame.display.flip()  # Update the display

        clock.tick(45)  # Set the frame rate to 45 FPS

    pygame.quit()  # Quit pygame properly
    sys.exit()  


if __name__ == "__main__":
    main()