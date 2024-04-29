import pygame
import random

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = (0, 0, 255)  # Default color for obstacles

    def update(self):
        pass  # Placeholder for updating obstacle state, such as animation or movement over time

    def collision(self, player):
        return self.rect.colliderect(player.rect)
