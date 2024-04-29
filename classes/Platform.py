import pygame
import random

class Platform:
    def __init__(self, x, y):           
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 60, 15)
        self.color='green'

    def whatTheFrock(self):
        mode = random.randint(1, 3)  # Type one should be plain, two should back and forth 
                                      # three should break after a second or two  <--- do this last bc i need make collision first
        if mode == 1:
            pass  # Plain platform
        elif mode == 2:
            self.y_speed = random.choice([-1, 1]) * 2  # Move up or down
        else:
            self.breakable = True

    def update_height(self):
        pass  # Placeholder. Will manipulate objects within the Platform class in accordance with the player.

        # Example: Move the platform down if it's moving
        if hasattr(self, 'y_speed'):
            self.y += self.y_speed

        # Example: Handle platform breaking
        if hasattr(self, 'breakable'):
            if self.breakable and time_since_platform_creation > 2000:  # Assuming time_since_platform_creation is in milliseconds
                # Platform breaks after 2 seconds
                self.color = 'red'  # Change color to indicate breaking
                # Handle breaking animation or logic here

# Example usage:
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

platform = Platform(400, 300)
time_since_platform_creation = 0

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    time_since_platform_creation += clock.tick(60)

    platform.update_height()

    pygame.draw.rect(screen, pygame.Color(platform.color), platform.rect)
    pygame.display.flip()

pygame.quit()
