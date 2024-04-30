import pygame

# Named variables
SCREEN_BOTTOM = 700
SCREEN_LEFT = 0
SCREEN_RIGHT = 415
SCREEN_X_MIDDLE = 50

GRAVITY_ACCELERATION = 1.25
JUMPING_STRENGTH = 50

class Player:
    # Constructor for Player class
    def __init__(self):
        # Hitbox radius
        self.radius = 10

        # Player's coordinates and moving speed
        self.x = SCREEN_X_MIDDLE
        self.y = 0
        self.speed = 10

        # Gravity controls
        self.is_on_surface = True
        self.is_jumping = False
        self.current_falling_speed = 1
        self.current_jumping_strength = JUMPING_STRENGTH


        # Sprite animation frames
        characterPath = "images/character"
        self.sprites_right = [pygame.image.load(f"{characterPath}/R1Pluto.png"), pygame.image.load(f"{characterPath}/R2Pluto.png"),
                 pygame.image.load(f"{characterPath}/R3Pluto.png"), pygame.image.load(f"{characterPath}/R4Pluto.png") ]
        self.sprites_left = [pygame.image.load(f"{characterPath}/L1Pluto.png"), pygame.image.load(f"{characterPath}/L2Pluto.png"),
                pygame.image.load(f"{characterPath}/L3Pluto.png"), pygame.image.load(f"{characterPath}/L4Pluto.png")]
        self.sprites_idle = [pygame.image.load(f"{characterPath}/I1Pluto.png"), pygame.image.load(f"{characterPath}/I2Pluto.png"),
                        pygame.image.load(f"{characterPath}/I3Pluto.png"), pygame.image.load(f"{characterPath}/I4Pluto.png")]

        # Variables to store player's current direction, for the sprite animations
        self.current_direction = "idle"
        self.current_sprites = self.sprites_idle # current sprite list
        self.current_frame = 0 # current index of the sprite frames
        
        self.sprite_rect = self.sprites_right[0].get_rect(center=[0,800]) # Get sprite rectangle

    def __str__(self): #toString method for hitbox testing later
        return "My name is Pluto! I'm currently at the coordinates " + str(self.x)+", "+ str(self.y)+ ". My speed is "+str(self.speed)+" and my position is " +self.current_direction
        
    def move(self, pixels_to_move):
        self.x += pixels_to_move

        # Amount of pixels the player has to move off-screen to teletransport to the other side
        LOOPING_OFFSET = 20

        # Moves the player to the other side of the screen if it moves too far
        if self.x <= SCREEN_LEFT - LOOPING_OFFSET * 2:
            self.x = SCREEN_RIGHT
        elif self.x >= SCREEN_RIGHT + LOOPING_OFFSET:
            self.x = SCREEN_LEFT


    def jump(self, is_gravity_call = False):
        if self.is_on_surface or is_gravity_call: # Only execute if the player is on a "floor" or the function is being called by the applyGravity function
            self.is_on_surface = False
            self.is_jumping = True
            
            # Update player's y coordinate
            self.y -= self.current_jumping_strength

            # Make jumping strength weaker
            self.current_jumping_strength *= .8

            # If the jumping strength is too weak, stop going up
            if self.current_jumping_strength < 1:
                self.is_jumping = False

                # Reset jumping strength for next jump
                self.current_jumping_strength = JUMPING_STRENGTH

    # Surfaces has to be an array with the coordinates of the platforms and screen bottom
    # Method that's called frame
    def tick(self, surfaces = []):
        self.animatePlayerImage()

        if self.is_jumping:
            self.jump(is_gravity_call=True)
        else:
            self.fall(surfaces)
            

    def isOnPlatform(self, platforms):
        player_is_on_platform = False
        surfaceYPosition = 0
        for surface in platforms:
            if self.x >= surface.x and self.x <= surface.x + surface.width and self.y == surface.y:
                player_is_on_platform = True
                surfaceYPosition = surface.y
                break

        return player_is_on_platform, surfaceYPosition

    def fall(self, surfaces):
        # Check is the player is on a surface
        isOnPlatform, platformYPosition = self.isOnPlatform(surfaces)
        
        if self.y < SCREEN_BOTTOM and not isOnPlatform:
            self.is_falling = True

            self.current_falling_speed *= GRAVITY_ACCELERATION
            self.y += self.current_falling_speed

        else: 
            self.is_on_surface = True
            self.is_falling = False

            if isOnPlatform:
                self.y = platformYPosition
            else:
                self.y = SCREEN_BOTTOM

            # Reset falling speed
            self.current_falling_speed = 1
            
    # Function to update player's animation
    def animatePlayerImage(self):
        self.current_frame += 0.2

        if self.current_frame >= len(self.current_sprites): 
            self.current_frame = 0