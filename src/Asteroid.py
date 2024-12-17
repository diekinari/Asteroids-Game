import random
from PIL import Image, ImageTk
import os
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

        self.angular_speed = random.uniform(-2, 2)
        self.angle = random.uniform(0, 360)

        original_asteroid_image = Image.open(os.path.join(SPRITE_FOLDER, "asteroid.png"))
        scaled_image = original_asteroid_image.resize(
            (self.radius * 2, self.radius * 2), Image.Resampling.LANCZOS
        )
        self.original_image = scaled_image
        self.image = ImageTk.PhotoImage(self.original_image)
        self.sprite_id = self.canvas.create_image(self.x, self.y, image=self.image)

        explosion_1_path = os.path.join(SPRITE_FOLDER, "explosion1.png")
        explosion_2_path = os.path.join(SPRITE_FOLDER, "explosion2.png")
        self.explosion_images = [
            ImageTk.PhotoImage(Image.open(explosion_1_path).resize((self.radius * 2, self.radius * 2))),
            ImageTk.PhotoImage(Image.open(explosion_2_path).resize((self.radius * 2, self.radius * 2))),
        ]

        self.exploding = False
        self.explosion_timer = 0

    def update(self):
        if self.exploding:
            self.handle_explosion()
        elif not self.destroyed:
            self.update_position_and_rotation()

    def update_position_and_rotation(self):
        self.x = (self.x + self.velocity_x) % SCREEN_WIDTH
        self.y = (self.y + self.velocity_y) % SCREEN_HEIGHT

        self.angle = (self.angle + self.angular_speed) % 360
        rotated_image = self.original_image.rotate(self.angle, resample=Image.Resampling.BICUBIC)
        self.image = ImageTk.PhotoImage(rotated_image)
        self.canvas.itemconfig(self.sprite_id, image=self.image)

        self.canvas.coords(self.sprite_id, self.x, self.y)

    def start_explosion(self, mark_as_killer=False):
        # print(f"Asteroid {self.sprite_id} starting explosion.")
        self.exploding = True
        self.explosion_timer = 0
        self.canvas.itemconfig(self.sprite_id, image=self.explosion_images[0])

        if not mark_as_killer:
            self.destroyed = True

    def handle_explosion(self):
        # print(f"Asteroid {self.sprite_id} exploding. Timer: {self.explosion_timer}")
        self.explosion_timer += 1
        if self.explosion_timer == 10:
            # print(f"Asteroid {self.sprite_id} switching to second explosion frame.")
            self.canvas.itemconfig(self.sprite_id, image=self.explosion_images[1])
        elif self.explosion_timer >= 20:
            # print(f"Asteroid {self.sprite_id} explosion complete.")
            self.exploding = False
            self.destroyed = True
