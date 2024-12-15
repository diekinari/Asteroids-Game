import math

from src.Rocket import Rocket
from src.config import *


class Ship:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.angle = 0
        self.radius = 15
        self.velocity_x = 0
        self.velocity_y = 0
        self.thrusting = False
        self.id = self.canvas.create_polygon(x, y - self.radius, x - self.radius, y + self.radius,
                                             x + self.radius, y + self.radius, fill="blue")

    def update(self):
        # Apply thrust if thrusting  
        if self.thrusting:
            self.velocity_x += SHIP_THRUST * math.cos(math.radians(self.angle))
            self.velocity_y += SHIP_THRUST * math.sin(math.radians(self.angle))
        else:
            self.velocity_x *= 0.99  # Apply friction  
            self.velocity_y *= 0.99

            # Update position with wrapping  
        self.x = (self.x + self.velocity_x) % SCREEN_WIDTH
        self.y = (self.y + self.velocity_y) % SCREEN_HEIGHT

        # Calculate rotated coordinates  
        nose_x = self.x + self.radius * math.cos(math.radians(self.angle))
        nose_y = self.y + self.radius * math.sin(math.radians(self.angle))
        left_x = self.x + self.radius * math.cos(math.radians(self.angle + 135))
        left_y = self.y + self.radius * math.sin(math.radians(self.angle + 135))
        right_x = self.x + self.radius * math.cos(math.radians(self.angle - 135))
        right_y = self.y + self.radius * math.sin(math.radians(self.angle - 135))

        # Update ship's position on the canvas  
        self.canvas.coords(self.id, nose_x, nose_y, left_x, left_y, right_x, right_y)

    def rotate(self, angle):
        self.angle = (self.angle + angle) % 360

    def shoot(self):
        nose_x = self.x + self.radius * math.cos(math.radians(self.angle))
        nose_y = self.y + self.radius * math.sin(math.radians(self.angle))
        return Rocket(self.canvas, nose_x, nose_y, self.angle)

    def respawn(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.velocity_x = 0
        self.velocity_y = 0