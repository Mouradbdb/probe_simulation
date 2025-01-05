# src/mass.py

import pygame
from settings import BLUE, DARK_BLUE, DARK_RED

class Mass:
    def __init__(self, x, y, mass, radius, color=BLUE):
        """
        Initialize a mass object that exerts gravitational force.
        x, y: Position in world coordinates
        mass: Mass of the object
        radius: Radius for visual representation
        color: Color for the mass
        """
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color

    def draw(self, surface, camera_offset):
        """
        Draw the mass on the given surface with camera offset.
        Adds a glow effect for better visibility.
        """
        screen_x = self.x + camera_offset[0]
        screen_y = self.y + camera_offset[1]

        # Draw glow
        for i in range(5, 15):
            alpha = max(0, 255 - i * 15)
            glow_color = (*self.color, alpha)
            glow_surface = pygame.Surface((self.radius*2 + i*2, self.radius*2 + i*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, glow_color, (self.radius + i, self.radius + i), self.radius + i)
            surface.blit(glow_surface, (screen_x - self.radius - i, screen_y - self.radius - i), special_flags=pygame.BLEND_RGBA_ADD)

        # Draw the main mass
        pygame.draw.circle(surface, self.color, (int(screen_x), int(screen_y)), self.radius)
