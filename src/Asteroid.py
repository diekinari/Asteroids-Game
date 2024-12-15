import random

from src.config import *


class Asteroid:
    def __init__(self, canvas, x, y, dx, dy):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.velocity_x = dx
        self.velocity_y = dy
        self.radius = random.randint(20, 40)
        self.destroyed = False
        self.id = self.canvas.create_oval(x - self.radius, y - self.radius,
                                          x + self.radius, y + self.radius, fill="gray")

    def update(self):
        if self.destroyed:
            self.canvas.delete(self.id)
        else:
            self.x = (self.x + self.velocity_x) % SCREEN_WIDTH
            self.y = (self.y + self.velocity_y) % SCREEN_HEIGHT
            self.canvas.coords(self.id, self.x - self.radius, self.y - self.radius,
                               self.x + self.radius, self.y + self.radius)