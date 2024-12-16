import math
from PIL import Image, ImageTk
import os
from src.config import *


class Rocket:
    def __init__(self, canvas, x, y, angle):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.angle = angle
        self.velocity_x = ROCKET_SPEED * math.cos(math.radians(angle))
        self.velocity_y = ROCKET_SPEED * math.sin(math.radians(angle))
        self.lifetime = ROCKET_LIFETIME
        self.expired = False

        original_rocket_image = Image.open(os.path.join(SPRITE_FOLDER, "rocket.png"))
        rotated_image = original_rocket_image.rotate(angle, resample=Image.BICUBIC)
        self.image = ImageTk.PhotoImage(rotated_image)

        self.sprite_id = self.canvas.create_image(self.x, self.y, image=self.image)

    def update(self):
        self.x = (self.x + self.velocity_x) % SCREEN_WIDTH
        self.y = (self.y + self.velocity_y) % SCREEN_HEIGHT
        self.canvas.coords(self.sprite_id, self.x, self.y)
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.expired = True
            self.canvas.delete(self.sprite_id)
