import math
from PIL import Image, ImageTk
import os

from src.Rocket import Rocket
from src.config import *


class Ship:
    def __init__(self, canvas, x, y, sprites):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.angle = 270
        self.radius = 30
        self.velocity_x = 0
        self.velocity_y = 0
        self.thrusting = False
        self.sprites = sprites
        self.original_static_ship = Image.open(os.path.join(SPRITE_FOLDER, "new_static_ship.png")).resize((60, 60),
                                                                                                          Image.Resampling.LANCZOS)
        self.original_thrusting_ship = Image.open(os.path.join(SPRITE_FOLDER, "new_thrusting_ship.png")).resize(
            (60, 60), Image.Resampling.LANCZOS)

        self.current_image = None
        self.update_image()

    def update_image(self):
        sprite_to_use = (
            self.original_thrusting_ship if self.thrusting else self.original_static_ship
        )
        rotated_image = sprite_to_use.rotate(-(self.angle - 90), resample=Image.BICUBIC)
        self.current_image = ImageTk.PhotoImage(rotated_image)
        if hasattr(self, 'sprite_id'):
            self.canvas.itemconfig(self.sprite_id, image=self.current_image)
        else:
            self.sprite_id = self.canvas.create_image(self.x, self.y, image=self.current_image)

    def update(self):
        if self.thrusting:
            self.velocity_x += SHIP_THRUST * math.cos(math.radians(self.angle))
            self.velocity_y += SHIP_THRUST * math.sin(math.radians(self.angle))
        else:
            self.velocity_x *= 0.99  
            self.velocity_y *= 0.99

        self.x = (self.x + self.velocity_x) % SCREEN_WIDTH
        self.y = (self.y + self.velocity_y) % SCREEN_HEIGHT

        self.update_image()
        self.canvas.coords(self.sprite_id, self.x, self.y)

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