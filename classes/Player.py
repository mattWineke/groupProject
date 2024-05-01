import pygame

# Named variables
SCREEN_BOTTOM = 700
SCREEN_LEFT = -15
SCREEN_RIGHT = 400

STARTING_X_POSITION = 50

GRAVITY_ACCELERATION = 1.25
MAXIMUM_FALLING_SPEED = 40
JUMPING_STRENGTH = 50

CAMERA_FOLLOW_OFFSET = SCREEN_BOTTOM - 150  # Position where the camera will place pluto when moving

class Player:
    # Constructor for Player class
    def __init__(self):
        # Player's coordinates
        self.x = STARTING_X_POSITION
        self.y = SCREEN_BOTTOM

        # Camera control - updates when getting on platform
        self.camera_y_offset = 0
        self.target_camera_y_offset = 0
        
        # Player's moving speed
        self.speed = 10

        # Gravity controls
        self.is_on_surface = True
        self.is_jumping = False
        self.current_falling_speed = 1
        self.current_jumping_strength = JUMPING_STRENGTH

        
        # Lists with Sprite animation frames
        load = pygame.image.load
        characterPath = "images/character"

        self.sprites_right = [load(f"{characterPath}/R1Pluto.png"), load(f"{characterPath}/R2Pluto.png"),
                 load(f"{characterPath}/R3Pluto.png"), load(f"{characterPath}/R4Pluto.png") ]
        self.sprites_left = [load(f"{characterPath}/L1Pluto.png"), load(f"{characterPath}/L2Pluto.png"),
                load(f"{characterPath}/L3Pluto.png"), load(f"{characterPath}/L4Pluto.png")]
        self.sprites_idle = [load(f"{characterPath}/I1Pluto.png"), load(f"{characterPath}/I2Pluto.png"),
                        load(f"{characterPath}/I3Pluto.png"), load(f"{characterPath}/I4Pluto.png")]

        # Variables to store player's current direction, for the sprite animations
        self.current_direction = "idle"
        self.current_sprites = self.sprites_idle # Current sprite list
        self.current_frame = 0 # Current index of the sprite frames
        
        self.sprite_rect = self.sprites_right[0].get_rect(center=[self.x, self.y])

        # Player's dimensions
        self.width = self.sprite_rect.width
        self.height = self.sprite_rect.height
        

    def __str__(self): #toString method for testing
        return "Coordinates: " + str(self.x) + ", " + str(self.y) + ". Speed: "+ str(self.speed)+". Direction: " + self.current_direction + "."

    # Method that's called every frame
    def tick(self, surfaces = []):
        self.animatePlayerImage()
        self.animateCameraMovement()

        if self.is_jumping:
            self.jump(is_tick_call=True)
        else:
            self.fall(surfaces)
        
    def move(self, pixels_to_move):
        self.x += pixels_to_move

        # Amount of pixels the player has to move off-screen to teletransport to the other side
        LOOPING_OFFSET = 5

        # Moves the player to the other side of the screen if it moves too far
        if self.x <= SCREEN_LEFT - LOOPING_OFFSET:
            self.x = SCREEN_RIGHT

        elif self.x >= SCREEN_RIGHT + LOOPING_OFFSET:
            self.x = SCREEN_LEFT


    def jump(self, is_tick_call = False):
        if self.is_on_surface or is_tick_call: # Only execute if the player is on a surface or the function is being called by the tick function
            self.is_on_surface = False
            self.is_jumping = True
            
            # Update player's y-coordinate
            self.y -= self.current_jumping_strength

            # Make jumping strength weaker
            self.current_jumping_strength /= GRAVITY_ACCELERATION

            # If the jumping strength is too weak, stop going up
            if self.current_jumping_strength < 1:
                self.is_jumping = False

                # Reset jumping strength for next jump
                self.current_jumping_strength = JUMPING_STRENGTH

    # Method to check if the player is standing on a platform
    def isOnPlatform(self, platforms):
        player_is_on_platform = False
        
        # Variable to store y position of the platform where the player is standing
        platformYPosition = 0
        
        # Create a rectangle with pluto's dimensions to check if it collides with a platform
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for platform in platforms:
            # Create a rectangle for each platform considering pluto's width
            platform_rect = pygame.Rect(platform.x + self.width / 2.5, platform.y, platform.width - self.width / 2, platform.height)

            if player_rect.colliderect(platform_rect):
                player_is_on_platform = True
                platformYPosition = platform.y - platform.height

                # Break the platform if it has breakable type
                if platform.type == "breakable":
                    platform.broken = True

                # Adjust camera
                self.target_camera_y_offset = CAMERA_FOLLOW_OFFSET - self.y
                    
                break

        return player_is_on_platform, platformYPosition - self.width

    def fall(self, surfaces):
        # Check is the player is on a platform
        isOnPlatform, platformYPosition = self.isOnPlatform(surfaces)
        
        if self.y < SCREEN_BOTTOM and not isOnPlatform:
            self.is_on_surface = False
            self.is_falling = True

            self.current_falling_speed *= GRAVITY_ACCELERATION
            self.y += min(self.current_falling_speed, MAXIMUM_FALLING_SPEED)

        else: 
            self.is_on_surface = True
            self.is_falling = False

            # Player fell on a platform
            if isOnPlatform:
                self.y = platformYPosition

            # Player fell on the bottom of the screen
            else:
                self.y = SCREEN_BOTTOM

                # Adjust camera
                self.target_camera_y_offset = 0

            # Reset falling speed
            self.current_falling_speed = 1
            
    # Function to update player's animation
    def animatePlayerImage(self):
        self.current_frame += 0.2

        if self.current_frame >= len(self.current_sprites): 
            self.current_frame = 0

    # Function to animate camera's movement smoothly
    def animateCameraMovement(self):
        movingDistance = self.target_camera_y_offset - self.camera_y_offset

        # Player reached a new platform
        if movingDistance > 0:
            self.camera_y_offset += max(movingDistance / 5, 5)
            
        # Player fell back to initial position
        elif movingDistance < 0 and self.target_camera_y_offset == 0:
            self.camera_y_offset -= max(movingDistance / 5, 5)

            # Ensure the camera does not go below 0
            self.camera_y_offset = max(self.camera_y_offset, 0)