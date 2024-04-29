import pygame
import random

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = (255, 0, 0)  # Default color for power-ups
        self.type = random.choice(['jump_high', 'double_jump', 'invincibility'])  # Randomly choose type of power-up

    def apply_effect(self, player):
        if self.type == 'jump_high':
            player.jump_height *= 1.5  # Increase player's jump height by 50%
        elif self.type == 'double_jump':
            player.double_jump = True  # Enable double jump for player
        elif self.type == 'invincibility':
            player.invincible = True  # Make player invincible for a short duration

    def update(self):
        pass  # Placeholder for updating power-up state, such as animation or effects over time
