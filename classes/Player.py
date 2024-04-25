import pygame

class Player:
    def __init__(self, x, y):  #default constructor

        # The sprite animation frames
        characterPath = "images/character"
        self.sprites_right = [pygame.image.load(f"{characterPath}/R1Pluto.png"), pygame.image.load(f"{characterPath}/R2Pluto.png"),
                 pygame.image.load(f"{characterPath}/R3Pluto.png"), pygame.image.load(f"{characterPath}/R4Pluto.png") ]
        self.sprites_left = [pygame.image.load(f"{characterPath}/L1Pluto.png"), pygame.image.load(f"{characterPath}/L2Pluto.png"),
                pygame.image.load(f"{characterPath}/L3Pluto.png"), pygame.image.load(f"{characterPath}/L4Pluto.png")]
        self.sprites_idle = [pygame.image.load(f"{characterPath}/I1Pluto.png"), pygame.image.load(f"{characterPath}/I2Pluto.png"),
                        pygame.image.load(f"{characterPath}/I3Pluto.png"), pygame.image.load(f"{characterPath}/I4Pluto.png")]

        # PLayer current direction, for the sprite animations
        self.current_direction = "idle"
        self.current_sprites = self.sprites_idle # current sprite list
        self.current_frame = 0 # current index of the sprite frames
        
        self.sprite_rect = self.sprites_right[0].get_rect(center=[0,800])# Get sprite rectangle
        self.radius=10
        self.x = x
        self.y = y
        self.speed = 10
        self.is_jumping = False
        self.jump_height = 50
        self.jump_count = 10


    def __str__(self): #toString method for hitbox testing later
        return "My name is Pluto! I'm currently at the coordinates " +str(self.x)+", "+ str(self.y)+ ". My speed is "+str(self.speed)+" and my position is " +self.current_direction
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_count = self.jump_height

    def update_jump(self):
        if self.is_jumping:
            if self.jump_count > 0:
                self.y -= 5  # Adjust to control the jump height
                self.jump_count -= 1
            elif self.y < 700:  # Check if player is above the bottom of the screen
                self.y += 15  # Adjust to control the fall speed
            else:
                self.is_jumping = False
                self.jump_count = self.jump_height

    def loop(player):          #moves the object to the other side of the screen if they move too far
        if player.x <= -40:
            player.x = 418
        if player.x >= 420:
            player.x = -39

    def movePlayer(player):
        frame_rate = 10 #animation speed
        current_frame = 0
        clock = pygame.time.Clock()

        keys = pygame.key.get_pressed()

        player.current_direction = "idle"
        player.current_sprites = player.sprites_idle #fall back to idle sprite list unless keys are being pressed
        
        if keys[pygame.K_LEFT]: 
            player.current_direction = "left"
            player.current_sprites = player.sprites_left # make the current sprite list left
            current_frame += 0.2
            player.move(-player.speed, 0)

        if keys[pygame.K_RIGHT]:
            player.current_direction = "right"
            player.current_sprites = player.sprites_right # make the current sprite list right
            current_frame += 0.2
            player.move(player.speed, 0)


        if keys[pygame.K_UP]:
            player.y-=10  # Maybe freeze here
        if keys[pygame.K_DOWN]:
            player.move(0, player.speed)
        if keys[pygame.K_SPACE]:
            player.jump()
            print(player.x,"",player.y)
        if keys[pygame.K_p]:
            print (player)

        # Allow movement during jump
        if player.is_jumping:  # Check if the player is currently jumping
            if keys[pygame.K_LEFT]:  # Allow left movement during jump
                player.move(-player.speed, 0)
            if keys[pygame.K_RIGHT]:  # Allow right movement during jump
                player.move(player.speed, 0)

    def animationLooping(player):
        
        player.current_frame += 0.2
        if player.current_frame >= len(player.current_sprites): 
            player.current_frame = 0
        if player.current_frame == 4:
            player.current_frame = 0