import pygame

class Button:
    # Constructor for Button class
    def __init__(self, text, x, y, width, height, font, color, backgroundColor, hoverColor, function, borderRadius):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.color = color
        self.background_color = backgroundColor
        self.hover_color = hoverColor
        self.function = function
        self.hovered = False
        self.border_radius = borderRadius

    # Method to draw the button on the screen
    def draw(self, surface):
        # Mouse controls
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        mouseIsHovering = self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height

        # Set button's color
        current_color = self.hover_color if mouseIsHovering else self.background_color

        # Draw rounded rectangle
        self.drawRoundedRectangle(surface, current_color)
        
        # Check if the button has been clicked
        if click[0] == 1 and mouseIsHovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.function()

        # Change cursor based on hover state
        if self.hovered and not (mouseIsHovering):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.hovered = False
        elif not self.hovered and mouseIsHovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.hovered = True

        # Draw the button's text
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text_surface, text_rect)

    # Method to draw a rectangle with rounded corners
    def drawRoundedRectangle(self, surface, color):
        # Draw a rectangle with clipped corners
        tall_rect = pygame.Rect(self.x + self.border_radius, self.y, self.width - 2 * self.border_radius, self.height)
        wide_rect = pygame.Rect(self.x, self.y + self.border_radius, self.width, self.height - 2 * self.border_radius)
        
        pygame.draw.rect(surface, color, tall_rect)
        pygame.draw.rect(surface, color, wide_rect)
        
        # Fill rectangle's corners with circles
        pygame.draw.circle(surface, color, (self.x + self.border_radius, self.y + self.border_radius), self.border_radius)
        pygame.draw.circle(surface, color, (self.x + self.width - self.border_radius, self.y + self.border_radius), self.border_radius)
        pygame.draw.circle(surface, color, (self.x + self.border_radius, self.y + self.height - self.border_radius), self.border_radius)
        pygame.draw.circle(surface, color, (self.x + self.width - self.border_radius, self.y + self.height - self.border_radius), self.border_radius)