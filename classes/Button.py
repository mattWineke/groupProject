import pygame

class Button:
    # Constructor for Button class
    def __init__(self, text, x, y, width, height, font, color, backgroundColor, hoverColor, function, borderRadius=5):
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
        draw_rounded_rect(surface, current_color, (self.x, self.y, self.width, self.height), self.border_radius)
        
        # Check if the button has been clicked
        if click[0] == 1 and mouseIsHovering:
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

# Function to draw a rectangle with rounded corners
def draw_rounded_rect(surface, color, rect, border_radius):
    # Draw the rectangle (rectangles)
    x, y, width, height = rect
    rect_main = pygame.Rect(x + border_radius, y, width - 2 * border_radius, height)
    rect_top = pygame.Rect(x, y + border_radius, width, height - 2 * border_radius)
    
    pygame.draw.rect(surface, color, rect_main)
    pygame.draw.rect(surface, color, rect_top)
    
    # Draw its corners
    pygame.draw.circle(surface, color, (x + border_radius, y + border_radius), border_radius)
    pygame.draw.circle(surface, color, (x + width - border_radius, y + border_radius), border_radius)
    pygame.draw.circle(surface, color, (x + border_radius, y + height - border_radius), border_radius)
    pygame.draw.circle(surface, color, (x + width - border_radius, y + height - border_radius), border_radius)