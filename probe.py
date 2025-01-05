# src/probe.py

import pygame
import math
from settings import WHITE, RED, SCALE_FACTOR, PURPLE


class Probe:
    def __init__(self, x, y):
        # Position in world coordinates
        self.x = x
        self.y = y

        # Velocity
        self.vx = 0.0
        self.vy = 0.0

        # Angle in degrees (0 degrees points to the right)
        self.angle = 0.0

        # Rotation speed (degrees per second)
        self.rotation_speed = 180  # Faster rotation for responsiveness

        # Thrust acceleration (pixels per second squared)
        self.thrust_acceleration = 100.0  # Reduced from 200.0

        # Maximum velocities
        self.max_vx = 300  # Reduced from 500
        self.max_vy = 300  # Reduced from 500

        # Probe dimensions (scaled down)
        self.width = int(40 * SCALE_FACTOR)
        self.height = int(60 * SCALE_FACTOR)

        # Thruster dimensions (scaled down)
        self.thruster_width = int(10 * SCALE_FACTOR)
        self.thruster_height = int(20 * SCALE_FACTOR)

        # Image Surface for the probe
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_probe()

        # Trajectory trail
        self.trajectory = []

    def draw_probe(self):
        """
        Draw the main body and thrusters of the probe onto its image surface.
        """
        # Draw the main body of the probe
        self.image.fill(WHITE)

        # Draw thrusters as rectangles at the back (left side)
        thruster_rect = pygame.Rect(
            0,  # Left edge
            self.height // 2 - self.thruster_height // 2,  # Vertically centered
            self.thruster_width,
            self.thruster_height
        )
        pygame.draw.rect(self.image, RED, thruster_rect)

    def rotate(self, direction, dt):
        """
        Rotate the probe.
        direction: 1 for left (counter-clockwise), -1 for right (clockwise)
        dt: Delta time in seconds
        """
        self.angle += direction * self.rotation_speed * dt
        self.angle %= 360  # Keep angle within [0, 360)

    def thrust(self, dt):
        """
        Apply thrust to the probe.
        dt: Delta time in seconds
        """
        # Calculate acceleration components based on current angle
        rad_angle = math.radians(self.angle)
        ax = math.cos(rad_angle) * self.thrust_acceleration
        ay = math.sin(rad_angle) * self.thrust_acceleration

        # Update velocities with acceleration
        self.vx += ax * dt
        self.vy += ay * dt

        # Cap velocities
        self.vx = max(-self.max_vx, min(self.vx, self.max_vx))
        self.vy = max(-self.max_vy, min(self.vy, self.max_vy))

    def apply_gravity(self, masses, dt):
        """
        Apply gravitational acceleration from multiple mass objects.
        masses: List of Mass instances
        dt: Delta time in seconds
        """
        total_ax = 0.0
        total_ay = 0.0
        for mass_obj in masses:
            # Calculate distance components
            dx = mass_obj.x - self.x
            dy = mass_obj.y - self.y
            distance_sq = dx**2 + dy**2
            distance = math.sqrt(distance_sq)

            # Prevent division by zero and set a minimum distance
            min_distance = mass_obj.radius + max(self.width, self.height)
            if distance < min_distance:
                distance = min_distance
                distance_sq = distance**2

            # Calculate gravitational force magnitude
            force = mass_obj.G * mass_obj.mass / distance_sq  # F = G * M / r^2

            # Calculate acceleration components
            ax = (force * dx) / distance  # a = F * (dx/r)
            ay = (force * dy) / distance  # a = F * (dy/r)

            # Sum up the total gravitational acceleration
            total_ax += ax
            total_ay += ay

        # Update probe's velocity with total gravitational acceleration
        self.vx += total_ax * dt
        self.vy += total_ay * dt

    def update_position(self, dt):
        """
        Update the probe's position based on its velocity.
        dt: Delta time in seconds
        """
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Update trajectory trail
        self.trajectory.append((self.x, self.y))
        if len(self.trajectory) > 500:
            self.trajectory.pop(0)

    def get_rotated_image(self):
        """
        Rotate the probe's image based on its current angle.
        Returns the rotated image and its new rectangle.
        """
        rotated_image = pygame.transform.rotate(self.image, -self.angle)  # Pygame rotates counter-clockwise, so invert angle
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        return rotated_image, rotated_rect

    def get_thruster_position(self):
        """
        Calculate the global position of the thruster based on the probe's current rotation.
        Returns (x, y) tuple.
        """
        # Local thruster position relative to probe center before rotation
        local_thruster_x = -self.width / 2  # Left side (back)
        local_thruster_y = 0  # Center vertically

        # Convert angle to radians
        rad_angle = math.radians(self.angle)

        # Rotate the local thruster position
        rotated_thruster_x = local_thruster_x * math.cos(rad_angle) - local_thruster_y * math.sin(rad_angle)
        rotated_thruster_y = local_thruster_x * math.sin(rad_angle) + local_thruster_y * math.cos(rad_angle)

        # Global thruster position
        global_thruster_x = self.x + rotated_thruster_x
        global_thruster_y = self.y + rotated_thruster_y

        return global_thruster_x, global_thruster_y

    def draw_trajectory(self, surface, camera_offset):
        """
        Draw the probe's trajectory trail.
        """
        if len(self.trajectory) > 1:
            points = [((x + camera_offset[0]), (y + camera_offset[1])) for x, y in self.trajectory]
            pygame.draw.lines(surface, PURPLE, False, points, 2)
