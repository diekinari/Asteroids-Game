from PIL import Image, ImageTk
import os

from src.config import *


class BackgroundAsteroid:
    def __init__(self, canvas, x, y, size, speed):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.image = ImageTk.PhotoImage(
            Image.open(os.path.join(SPRITE_FOLDER, "asteroid_old.png")).resize(
                (self.size, self.size), Image.Resampling.LANCZOS
            )
        )
        self.sprite_id = self.canvas.create_image(self.x, self.y, image=self.image)

    def update(self):
        self.x -= self.speed
        if self.x < -self.size:  # Wrap around the screen
            self.x = SCREEN_WIDTH + self.size
        self.canvas.coords(self.sprite_id, self.x, self.y)

    def remove(self):
        self.canvas.delete(self.sprite_id)
