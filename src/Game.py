import tkinter as tk
from PIL import Image, ImageTk
import os
import math
import random

from src.Asteroid import Asteroid
from src.Ship import Ship
from src.config import *


class Game:
    def __init__(self, root):
        self.thrusting = None
        self.rotating_right = None
        self.rotating_left = None
        self.root = root
        self.canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="black")
        self.canvas.pack()

        self.lives = LIVES
        self.score = INITIAL_SCORE
        self.running = False

        self.heart_images = []
        self.heart_widgets = []

        self.score_text = self.canvas.create_text(10, 10, anchor="nw", fill="white",
                                                  font=("Arial", 16), text=f"Score: {self.score}")

        self.asteroids = []
        self.rockets = []
        self.ship = None

        self.start_screen = self.canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                                    fill="white", font=("Arial", 24),
                                                    text="Click to Start")
        self.canvas.tag_bind(self.start_screen, "<Button-1>", self.start_game)

        self.sprites = self.load_sprites()
        self.heart_image = self.sprites["heart"]

        self.root.bind("<KeyPress-Left>", lambda event: self.set_rotation(-1))
        self.root.bind("<KeyRelease-Left>", lambda event: self.set_rotation(0))
        self.root.bind("<KeyPress-Right>", lambda event: self.set_rotation(1))
        self.root.bind("<KeyRelease-Right>", lambda event: self.set_rotation(0))
        self.root.bind("<KeyPress-Up>", lambda event: self.set_thrust(True))
        self.root.bind("<KeyRelease-Up>", lambda event: self.set_thrust(False))
        self.root.bind("<space>", lambda event: self.shoot_rocket())

        self.game_over_in_progress = False

    def load_sprites(self):
        sprites = {}
        heart_path = os.path.join(SPRITE_FOLDER, HEART_IMAGE_FILENAME)
        sprites["heart"] = ImageTk.PhotoImage(
            Image.open(heart_path).resize((HEART_IMAGE_SIZE, HEART_IMAGE_SIZE))
        )
        static_ship_path = os.path.join(SPRITE_FOLDER, "static_ship.png")
        thrusting_ship_path = os.path.join(SPRITE_FOLDER, "thrusting_ship.png")
        sprites["static_ship"] = ImageTk.PhotoImage(Image.open(static_ship_path))
        sprites["thrusting_ship"] = ImageTk.PhotoImage(Image.open(thrusting_ship_path))
        return sprites

    def update_heart_display(self):
        # Clear existing heart widgets
        for widget in self.heart_widgets:
            self.canvas.delete(widget)
        self.heart_widgets.clear()

        for i in range(self.lives):
            x_offset = SCREEN_WIDTH - (i + 1) * (HEART_IMAGE_SIZE + 5) - 10
            y_offset = 10
            heart = self.canvas.create_image(x_offset, y_offset, anchor="nw", image=self.heart_image)
            self.heart_widgets.append(heart)

    def set_rotation(self, direction):
        if direction == -1:
            self.rotating_left = True
            self.rotating_right = False
        elif direction == 1:
            self.rotating_left = False
            self.rotating_right = True
        else:
            self.rotating_left = False
            self.rotating_right = False

    def set_thrust(self, thrusting):
        self.thrusting = thrusting

    def start_game(self, event):
        if not self.running:
            self.running = True
            self.canvas.delete(self.start_screen)
            self.reset_game()
            self.ship = Ship(self.canvas, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.sprites)
            self.spawn_asteroids()
            self.update_game()

    def reset_game(self):
        self.lives = LIVES
        self.score = INITIAL_SCORE
        self.update_heart_display()
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def update_game(self):
        if self.running:
            # Update ship state
            if self.ship:
                if self.rotating_left:
                    self.ship.rotate(-SHIP_ROTATION_SPEED)
                if self.rotating_right:
                    self.ship.rotate(SHIP_ROTATION_SPEED)

                self.ship.thrusting = self.thrusting
                self.ship.update()

            self.update_rockets()
            self.update_asteroids()
            self.check_collisions()
            self.cleanup_objects()

            if not self.game_over_in_progress:
                self.spawn_asteroids()

            self.root.after(16, self.update_game)

    def cleanup_objects(self):
        for rocket in self.rockets:
            if rocket.expired:
                self.canvas.delete(rocket.sprite_id)
        self.rockets = [r for r in self.rockets if not r.expired]

        for asteroid in self.asteroids:
            if asteroid.destroyed and not asteroid.exploding:
                self.canvas.delete(asteroid.sprite_id)
        self.asteroids = [a for a in self.asteroids if not (a.destroyed and not a.exploding)]

    def check_collisions(self):
        for rocket in self.rockets:
            for asteroid in self.asteroids:
                if self.distance(rocket.x, rocket.y, asteroid.x, asteroid.y) < asteroid.radius:
                    print(f"Collision detected: Rocket {rocket.sprite_id} hit Asteroid {asteroid.sprite_id}")
                    rocket.expired = True
                    if not asteroid.exploding:
                        print(f"Asteroid {asteroid.sprite_id} starts explosion")
                        asteroid.start_explosion()
                    self.score += 1
                    self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                    break

        if self.ship:
            for asteroid in self.asteroids:
                # Skip exploding asteroids
                if asteroid.exploding:
                    continue

                if self.distance(self.ship.x, self.ship.y, asteroid.x, asteroid.y) < asteroid.radius:
                    # print(f"Collision detected: Ship collided with Asteroid {asteroid.sprite_id}")
                    if not asteroid.exploding:
                        asteroid.start_explosion(mark_as_killer=True)
                    self.lives -= 1
                    self.update_heart_display()
                    if self.lives <= 0:
                        self.game_over()
                        return
                    else:
                        self.ship.respawn()

    def update_rockets(self):
        for rocket in self.rockets:
            rocket.update()
        self.rockets = [r for r in self.rockets if not r.expired]

    def update_asteroids(self):
        for asteroid in self.asteroids:
            asteroid.update()
        self.asteroids = [a for a in self.asteroids if not (a.destroyed and not a.exploding)]

    def spawn_asteroids(self):
        if not self.running or self.game_over_in_progress:  # Prevent spawning during game over
            return

        num_to_spawn = max(0, MIN_ASTEROIDS - len(self.asteroids))
        for _ in range(num_to_spawn):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            dx = random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED)
            dy = random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED)
            self.asteroids.append(Asteroid(self.canvas, x, y, dx, dy))

        self.asteroids = self.asteroids[:MAX_ASTEROIDS]

    def game_over(self):
        # print("Game Over! Finalizing animations...")
        self.game_over_in_progress = True

        # Remove the ship immediately
        if self.ship and hasattr(self.ship, 'sprite_id'):
            self.canvas.delete(self.ship.sprite_id)
            self.ship = None

        for asteroid in self.asteroids:
            if not asteroid.exploding:  # Keep only the killer asteroid
                self.canvas.delete(asteroid.sprite_id)
        self.asteroids = [a for a in self.asteroids if a.exploding]

        self.canvas.delete(self.score_text)

        self.wait_for_explosions()

    def wait_for_explosions(self):
        """Wait until all explosions are finished before displaying the final Game Over screen."""
        explosions_active = any(asteroid.exploding for asteroid in self.asteroids)

        if explosions_active:
            self.root.after(100, self.wait_for_explosions)
        else:
            self.finalize_game_over()

    def finalize_game_over(self):
        # Remove all remaining game elements
        for asteroid in self.asteroids:
            if hasattr(asteroid, 'sprite_id'):
                self.canvas.delete(asteroid.sprite_id)
        self.asteroids.clear()

        for rocket in self.rockets:
            if hasattr(rocket, 'sprite_id'):
                self.canvas.delete(rocket.sprite_id)
        self.rockets.clear()

        game_over_ascii = """
              _____                         ____                 
             / ____|                       / __ \                
            | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ 
            | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|
            | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   
             \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   
                """
        self.canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                fill="red", font=("Courier", 16, "bold"),
                                text=game_over_ascii, anchor="center")

        self.canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                                fill="white", font=("Arial", 18, "bold"),
                                text=f"Final Score: {self.score}", anchor="center")

        self.running = False
        # print("Game Over sequence completed.")

    def rotate_ship(self, angle):
        if self.running:
            self.ship.rotate(angle)

    def thrust_ship(self, thrusting):
        if self.running:
            self.ship.thrusting = thrusting

    def shoot_rocket(self):
        if self.running:
            self.rockets.append(self.ship.shoot())

    @staticmethod
    def distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
