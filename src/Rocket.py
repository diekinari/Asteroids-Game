import math

from src.config import *


class Rocket:
    def __init__(self, canvas, x, y, angle):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.angle = angle
        self.velocity_x = ROCKET_SPEED * math.cos(math.radians(angle))
        self.velocity_y = ROCKET_SPEED * math.sin(math.radians(angle))
        self.id = self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red")
        self.lifetime = ROCKET_LIFETIME
        self.expired = False

    def update(self):
        self.x = (self.x + self.velocity_x) % SCREEN_WIDTH
        self.y = (self.y + self.velocity_y) % SCREEN_HEIGHT
        self.canvas.coords(self.id, self.x - 2, self.y - 2, self.x + 2, self.y + 2)
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.expired = True
            self.canvas.delete(self.id)