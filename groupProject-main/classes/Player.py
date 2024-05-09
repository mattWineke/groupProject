import pygame

# Named variables
SCREEN_BOTTOM = 710
SCREEN_LEFT = -40
SCREEN_RIGHT = 390

STARTING_X_POSITION = 50

GRAVITY_ACCELERATION = 1.25
MAXIMUM_FALLING_SPEED = 40
JUMPING_STRENGTH = 50

CAMERA_FOLLOW_OFFSET = SCREEN_BOTTOM - 300  # Position where the camera will place pluto when moving

class Player:
    # Constructor for Player class
    def __init__(self, sprites):
        self.is_alive = True
        
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

        # Load sprites
        self.sprites_right = sprites["right"]
        self.sprites_left = sprites["left"]
        self.sprites_idle = sprites["idle"]

        # Player's state
        self.current_direction = "idle"
        self.current_sprites = self.sprites_idle
        self.current_frame = 0
        
        # Initialize sprite rectangle
        self.sprite_rect = self.current_sprites[self.current_frame].get_rect(topleft = (self.x, self.y))

        # Player's dimensions
        self.width = self.sprite_rect.width
        self.height = self.sprite_rect.height

        # Initialize player's hitbox
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        
    # Method that's called every frame
    def tick(self, platforms):
        self.updateHitbox()
        self.animatePlayerImage()
        self.animateCameraMovement()

        if self.is_jumping:
            self.jump(override_surface_condition=True)
        else:
            self.fall(platforms)

    # Method to manage player's x position
    def move(self, pixels_to_move):
        self.x += pixels_to_move

        # Amount of pixels the player has to move off-screen to appear on the other side
        LOOPING_OFFSET = 5

        # Moves the player to the other side of the screen if it moves too far
        if self.x <= SCREEN_LEFT - LOOPING_OFFSET:
            self.x = SCREEN_RIGHT

        elif self.x >= SCREEN_RIGHT + LOOPING_OFFSET:
            self.x = SCREEN_LEFT

    # Method to handle jump animation
    def jump(self, override_surface_condition = False):
        if self.is_on_surface or override_surface_condition:
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
        
        for platform in platforms:
            if self.hitbox.colliderect(platform.hitbox):
                player_is_on_platform = True
                platformYPosition = platform.y - self.height + 2 # Add 2 pixels to avoid character jounce glitch

                # Set platform's touched attribute to true
                platform.touched = True

                # Adjust camera
                self.target_camera_y_offset = CAMERA_FOLLOW_OFFSET - self.y
                    
                break

        return player_is_on_platform, platformYPosition

    # Method to handle falling animation
    def fall(self, platforms):
        # Check is the player is on a platform
        isOnPlatform, platformYPosition = self.isOnPlatform(platforms)
        
        if self.y < SCREEN_BOTTOM and not isOnPlatform or not self.is_alive:
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
            
    # Method to update player's hitbox
    def updateHitbox(self):
        TRIM_PX_LEFT = 15
        TRIM_PX_RIGHT = 15

        self.hitbox.update(self.x + TRIM_PX_LEFT, self.y, self.width - TRIM_PX_LEFT - TRIM_PX_RIGHT, self.height)

    # Method to update player's animation
    def animatePlayerImage(self):
        self.current_frame += 0.2

        if self.current_frame >= len(self.current_sprites): 
            self.current_frame = 0

    # Method to animate camera's movement smoothly
    def animateCameraMovement(self):
        movingDistance = self.target_camera_y_offset - self.camera_y_offset

        # Player reached a new platform
        if movingDistance > 0:
            self.camera_y_offset += max(movingDistance / 5, 5)
            
        # Player fell back to initial position
        elif movingDistance < 0 and self.target_camera_y_offset == 0:
            self.camera_y_offset -= max(movingDistance / 5, 10)

            # Ensure the camera does not go below 0
            self.camera_y_offset = max(self.camera_y_offset, 0)

    # Method that makes player fall through platforms
    def die(self):
        if self.is_alive:
            self.is_alive = False

            # Player does a tiny jump before falling
            self.current_jumping_strength = 15
            self.jump(override_surface_condition = True)

            # Reset falling speed
            self.current_falling_speed = 1

            # Rotate images 180 degrees and store them back to be used in rendering
            self.sprites_idle = [pygame.transform.rotate(img, 180) for img in self.sprites_idle]    
            self.sprites_right = [pygame.transform.rotate(img, 180) for img in self.sprites_right]
            self.sprites_left = [pygame.transform.rotate(img, 180) for img in self.sprites_left]