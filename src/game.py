import tkinter as tk
import math
import random

from src.Asteroid import Asteroid
from src.Ship import Ship
from src.config import *


class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="black")
        self.canvas.pack()

        # Game state variables
        self.lives = LIVES
        self.score = INITIAL_SCORE
        self.running = False

        # UI elements
        self.lives_text = self.canvas.create_text(10, 10, anchor="nw", fill="white",
                                                  font=("Arial", 16), text=f"Lives: {self.lives}")
        self.score_text = self.canvas.create_text(10, 30, anchor="nw", fill="white",
                                                  font=("Arial", 16), text=f"Score: {self.score}")

        # Background and game objects
        self.asteroids = []
        self.rockets = []
        self.ship = None

        # Start screen
        self.start_screen = self.canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                                    fill="white", font=("Arial", 24),
                                                    text="Click to Start")
        self.canvas.tag_bind(self.start_screen, "<Button-1>", self.start_game)

        # Bind controls
        self.root.bind("<Left>", lambda event: self.rotate_ship(-SHIP_ROTATION_SPEED))
        self.root.bind("<Right>", lambda event: self.rotate_ship(SHIP_ROTATION_SPEED))
        self.root.bind("<Up>", lambda event: self.thrust_ship(True))
        self.root.bind("<KeyRelease-Up>", lambda event: self.thrust_ship(False))
        self.root.bind("<space>", lambda event: self.shoot_rocket())

    def start_game(self, event):
        if not self.running:
            self.running = True
            self.canvas.delete(self.start_screen)
            self.reset_game()
            self.ship = Ship(self.canvas, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.spawn_asteroids()
            self.update_game()

    def reset_game(self):
        self.lives = LIVES
        self.score = INITIAL_SCORE
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def update_game(self):
        if self.running:
            self.ship.update()
            self.update_rockets()
            self.update_asteroids()
            self.check_collisions()
            self.root.after(16, self.update_game)

    def update_rockets(self):
        for rocket in self.rockets:
            rocket.update()
        self.rockets = [r for r in self.rockets if not r.expired]

    def update_asteroids(self):
        for asteroid in self.asteroids:
            asteroid.update()
        self.asteroids = [a for a in self.asteroids if not a.destroyed]

    def spawn_asteroids(self):
        for _ in range(5):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            dx = random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED)
            dy = random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED)
            self.asteroids.append(Asteroid(self.canvas, x, y, dx, dy))

    def check_collisions(self):
        # Check for collisions between rockets and asteroids
        for rocket in self.rockets:
            for asteroid in self.asteroids:
                if self.distance(rocket.x, rocket.y, asteroid.x, asteroid.y) < asteroid.radius:
                    rocket.expired = True
                    asteroid.destroyed = True
                    self.score += 1
                    self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                    break

                    # Check for collisions between the ship and asteroids
        for asteroid in self.asteroids:
            if self.distance(self.ship.x, self.ship.y, asteroid.x, asteroid.y) < asteroid.radius:
                asteroid.destroyed = True
                self.lives -= 1
                self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")
                self.ship.respawn()
                if self.lives <= 0:
                    self.game_over()

    def game_over(self):
        self.running = False
        self.canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, fill="red",
                                font=("Arial", 24), text="Game Over")

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
