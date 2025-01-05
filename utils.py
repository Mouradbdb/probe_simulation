# src/utils.py

import pygame
import math
from settings import CYAN

def draw_arrow(surface, color, start, end, arrow_size=10, width=2):
    """
    Draws an arrow from start to end points on the given surface.
    """
    pygame.draw.line(surface, color, start, end, width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - arrow_size * math.cos(angle - math.pi / 6),
            end[1] - arrow_size * math.sin(angle - math.pi / 6))
    right = (end[0] - arrow_size * math.cos(angle + math.pi / 6),
             end[1] - arrow_size * math.sin(angle + math.pi / 6))
    pygame.draw.polygon(surface, color, [end, left, right])

def load_image(path, scale=1.0):
    """
    Loads an image from the given path and scales it.
    """
    image = pygame.image.load(path).convert_alpha()
    if scale != 1.0:
        size = image.get_size()
        image = pygame.transform.scale(image, (int(size[0]*scale), int(size[1]*scale)))
    return image
