# src/main.py

import pygame
import sys
import math
import random

from settings import WIDTH, HEIGHT, BLACK, WHITE, GREEN, PURPLE, FPS, SCALE_FACTOR
from probe import Probe
from mass import Mass
from particle import Particle
from utils import draw_arrow


def draw_gravity_vectors(surface, probe, masses, camera_offset):
    """
    Draw arrows representing the gravitational forces from each mass acting on the probe.
    """
    for mass_obj in masses:
        # Calculate vector from probe to mass
        dx = mass_obj.x - probe.x
        dy = mass_obj.y - probe.y
        distance = math.hypot(dx, dy)

        # Normalize the vector
        if distance != 0:
            ux = dx / distance
            uy = dy / distance
        else:
            ux, uy = 0, 0

        # Calculate gravitational acceleration
        grav_acceleration = mass_obj.G * mass_obj.mass / (distance**2) if distance != 0 else 0

        # Scale the vector for visualization purposes
        vector_length = min(grav_acceleration, 100)  # Limit the length for visibility
        end_x = probe.x + ux * vector_length
        end_y = probe.y + uy * vector_length

        # Apply camera offset
        start_pos = (probe.x + camera_offset[0], probe.y + camera_offset[1])
        end_pos = (end_x + camera_offset[0], end_y + camera_offset[1])

        # Draw the line
        pygame.draw.line(surface, WHITE, start_pos, end_pos, 2)

        # Draw the arrowhead
        angle = math.atan2(uy, ux)
        arrow_size = 10
        left = (end_x + math.cos(angle + math.pi * 3 / 4) * arrow_size,
                end_y + math.sin(angle + math.pi * 3 / 4) * arrow_size)
        right = (end_x + math.cos(angle - math.pi * 3 / 4) * arrow_size,
                 end_y + math.sin(angle - math.pi * 3 / 4) * arrow_size)
        pygame.draw.polygon(surface, WHITE, [
            (end_pos[0], end_pos[1]),
            (left[0] + camera_offset[0], left[1] + camera_offset[1]),
            (right[0] + camera_offset[0], right[1] + camera_offset[1])
        ])

def main():
    # Initialize Pygame
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Probe Simulation with Multiple Gravities")

    # Clock
    clock = pygame.time.Clock()

    # Create a probe instance at the center of the world
    probe = Probe(0, 0)

    # Create multiple mass objects (e.g., planets)
    masses = [
        Mass(x=300, y=0, mass=50000, radius=50, color=(0, 0, 255)),        # Mass 1: Blue planet
        Mass(x=-400, y=150, mass=70000, radius=60, color=(0, 0, 139)),     # Mass 2: Dark Blue planet
        Mass(x=200, y=-300, mass=60000, radius=55, color=(139, 0, 0)),     # Mass 3: Dark Red planet
        # Add more masses as needed
    ]

    # Assign gravitational constant to each mass
    for mass in masses:
        mass.G = 6.67430e1  # Ensure each mass has access to G from settings

    # List to hold active particles
    particles = []

    # Font for telemetry
    font = pygame.font.SysFont(None, 24)

    # Generate background stars
    NUM_STARS = 500
    STAR_AREA = 3000  # Defines how far stars are spread in each direction
    stars = []
    for _ in range(NUM_STARS):
        star_x = random.randint(-STAR_AREA, STAR_AREA)
        star_y = random.randint(-STAR_AREA, STAR_AREA)
        stars.append((star_x, star_y))

    # Define a target point (optional)
    target_x, target_y = 1000, 1000  # Position in world coordinates
    successful_operation = False

    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        probe.rotate(direction=-1 if keys[pygame.K_LEFT] else 1 if keys[pygame.K_RIGHT] else 0, dt=dt)
        if keys[pygame.K_UP]:
            probe.thrust(dt)

        # Apply gravitational forces from all masses
        probe.apply_gravity(masses, dt)

        # Update probe's position
        probe.update_position(dt)

        # If thrusting, emit particles
        if keys[pygame.K_UP]:
            thruster_x, thruster_y = probe.get_thruster_position()
            emission_angle = (probe.angle + 180) % 360  # Directly opposite to facing direction
            for _ in range(3):  # Adjust number for density
                particles.append(Particle(thruster_x, thruster_y, emission_angle))

        # Update particles
        for particle in particles[:]:
            particle.update(dt)
            if particle.life <= 0:
                particles.remove(particle)

        # Calculate camera offset to center the probe
        camera_offset_x = WIDTH // 2 - probe.x
        camera_offset_y = HEIGHT // 2 - probe.y
        camera_offset = (camera_offset_x, camera_offset_y)

        # Clear screen
        screen.fill(BLACK)

        # Draw background stars with camera offset
        for star in stars:
            star_screen_x = star[0] + camera_offset[0]
            star_screen_y = star[1] + camera_offset[1]
            # Only draw stars that are within the screen boundaries
            if -5 < star_screen_x < WIDTH + 5 and -5 < star_screen_y < HEIGHT + 5:
                pygame.draw.circle(screen, WHITE, (int(star_screen_x), int(star_screen_y)), 1)

        # Draw mass objects
        for mass_obj in masses:
            mass_obj.draw(screen, camera_offset)

        # Draw gravitational force vectors
        draw_gravity_vectors(screen, probe, masses, camera_offset)

        # Draw particles
        for particle in particles:
            particle.draw(screen, camera_offset)

        # Draw probe
        rotated_image, rotated_rect = probe.get_rotated_image()
        # Calculate probe's screen position
        probe_screen_x = probe.x + camera_offset[0]
        probe_screen_y = probe.y + camera_offset[1]
        rotated_rect.center = (probe_screen_x, probe_screen_y)
        screen.blit(rotated_image, rotated_rect.topleft)

        # Draw trajectory
        probe.draw_trajectory(screen, camera_offset)

        # Draw target (optional)
        target_screen_x = target_x + camera_offset[0]
        target_screen_y = target_y + camera_offset[1]
        pygame.draw.circle(screen, GREEN, (int(target_screen_x), int(target_screen_y)), max(5, int(10 * SCALE_FACTOR)))

        # Check for mission completion
        distance = math.hypot(probe.x - target_x, probe.y - target_y)
        if distance < (10 * SCALE_FACTOR):
            successful_operation = True

        # Display telemetry
        vy_text = font.render(f"Vertical Velocity: {probe.vy:.2f} px/s", True, WHITE)
        vx_text = font.render(f"Horizontal Velocity: {probe.vx:.2f} px/s", True, WHITE)
        angle_text = font.render(f"Angle: {int(probe.angle)%360}°", True, WHITE)
        distance_text = font.render(f"Distance to Target: {int(distance)} px", True, WHITE)

        # Calculate total gravitational acceleration for telemetry
        total_grav_ax = 0.0
        total_grav_ay = 0.0
        for mass_obj in masses:
            dx = mass_obj.x - probe.x
            dy = mass_obj.y - probe.y
            distance_sq = dx**2 + dy**2
            distance = math.sqrt(distance_sq)
            if distance != 0:
                ax = mass_obj.G * mass_obj.mass * dx / (distance_sq * distance)
                ay = mass_obj.G * mass_obj.mass * dy / (distance_sq * distance)
                total_grav_ax += ax
                total_grav_ay += ay
        total_grav_acceleration = math.hypot(total_grav_ax, total_grav_ay)
        grav_text = font.render(f"Total Gravitational Acceleration: {total_grav_acceleration:.2f} px/s²", True, PURPLE)

        # Position telemetry on the screen
        screen.blit(vy_text, (10, 10))
        screen.blit(vx_text, (10, 30))
        screen.blit(angle_text, (10, 50))
        screen.blit(distance_text, (10, 70))
        screen.blit(grav_text, (10, 90))

        # Display mission status
        if successful_operation:
            status_text = font.render("Mission Accomplished! Press ESC to exit.", True, GREEN)
            screen.blit(status_text, (WIDTH//2 - status_text.get_width()//2, HEIGHT//2))

        # Update the display
        pygame.display.flip()

        # Exit conditions
        if successful_operation:
            # Allow exit with ESC
            if keys[pygame.K_ESCAPE]:
                running = False

if __name__ == "__main__":
        main()
