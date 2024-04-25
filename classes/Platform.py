import pygame
import random

class Platform:
    def __init__(self, x, y):           
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 60, 15)
        self.color='green'


    def whatTheFrock():
        mode=random.randint(1,3)  #Type one should be plain, two should back and forth 
                                  # three should break after a second or two  <--- do this last bc i need make collision first
        if mode==1:
            pass
        elif mode==2:
            pass
        else:
            pass

        
    def update_height(self): #this will manipulate objects within the Platform class in accordance to the player, this will require Groups which I can do unless ur bored
        pass