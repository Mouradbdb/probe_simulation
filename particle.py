# src/particle.py

import pygame
import math
import random
from settings import YELLOW, ORANGE, RED, SCALE_FACTOR

class Particle:
    def __init__(self, x, y, angle):
        """
        Initialize a particle.
        x, y: Starting position
        angle: Emission angle in degrees
        """
        self.x = x
        self.y = y
        # Randomize the initial velocity slightly for a natural spread effect
        speed = random.uniform(50, 150)  # pixels per second
        rad_angle = math.radians(angle)
        self.vx = speed * math.cos(rad_angle)
        self.vy = speed * math.sin(rad_angle)
        self.life = 1.0  # Particle life in seconds
        self.size = max(1, int(random.randint(1, 2) * SCALE_FACTOR))  # Scaled down size
        self.color = random.choice([YELLOW, ORANGE, RED])

    def update(self, dt):
        """
        Update the particle's position and life.
        dt: Delta time in seconds
        """
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt

    def draw(self, surface, camera_offset):
        """
        Draw the particle on the given surface with camera offset.
        surface: Pygame surface to draw the particle
        camera_offset: (x, y) tuple for camera position
        """
        if self.life > 0:
            # Fade out the particle
            alpha = max(0, min(255, int(255 * (self.life / 1.0))))
            particle_color = self.color + (alpha,)
            particle_surface = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, particle_color, (self.size, self.size), self.size)
            # Apply camera offset
            screen_x = self.x + camera_offset[0] - self.size
            screen_y = self.y + camera_offset[1] - self.size
            surface.blit(particle_surface, (screen_x, screen_y))
