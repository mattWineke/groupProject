# Functions to animate pygame objects when appearing and disappearing

import pygame

def animateTextInAndOut(surface, font, text, initial_size, max_size, color, center, total_duration, time_left, animation_duration):
    time_passed = total_duration - time_left

    # Calculate current text scale
    if time_passed < animation_duration:
        # Growing phase
        scale = 1 * (time_passed / animation_duration)
    elif time_passed >  total_duration - animation_duration:
        # Shrinking phase
        scale = 1 * ((total_duration - time_passed) / animation_duration)
    else:
        # Middle phase
        scale = 1

    # Ensure scale is between 0 and 1
    scale = max(0, min(1, scale))

    # Calculate font size and opacity (alpha value)
    size = int(initial_size + (max_size - initial_size) * scale)
    alpha = int(255 * scale)

    # Render the text
    text_surface = font.render(text, True, color)
    text_surface = pygame.transform.scale(text_surface, (size, size))
    text_surface.set_alpha(alpha)

    # Get the rect and set the position
    text_rect = text_surface.get_rect(center = center)

    # Display the text
    surface.blit(text_surface, text_rect)

def animateCircleInAndOut(surface, RGB_color, center, initial_radius, max_radius, max_alpha, total_duration, time_left, animation_duration):
    time_passed = total_duration - time_left

    # Calculate current circle scale
    if time_passed < animation_duration:
        # Growing phase
        scale = (time_passed / animation_duration)
    elif time_passed > total_duration - animation_duration:
        # Shrinking phase
        scale = ((total_duration - time_passed) / animation_duration)
    else:
        # Middle phase
        scale = 1

    # Ensure scale is between 0 and 1
    scale = max(0, min(1, scale))

    # Calculate radius and opacity (alpha value)
    radius = int(initial_radius + (max_radius - initial_radius) * scale)
    alpha = min(int(255 * scale), max_alpha)

    # Create a temporary surface with alpha support to draw the circle
    temp_surface = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)

    # Create an RGBA color tuple including the alpha value (opacity)
    rgba_color = RGB_color + (alpha,)

    # Draw the circle
    pygame.draw.circle(temp_surface, rgba_color, (radius, radius), radius)

    # Get the rect and set the position
    circle_rect = temp_surface.get_rect(center=center)

    # Display the circle
    surface.blit(temp_surface, circle_rect)