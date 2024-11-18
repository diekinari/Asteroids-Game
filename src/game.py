# game.py

import tkinter as tk
from config import *


class Game:
    def __init__(self, root):
        """Инициализация параметров окна и элементов интерфейса."""
        self.root = root
        self.root.title(GAME_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.resizable(False, False)

        # Переменные для жизней и очков
        self.lives = INITIAL_LIVES
        self.score = INITIAL_SCORE

        # Режим игры: "start_screen", "playing", "game_over"
        self.game_mode = "start_screen"

        # Создание интерфейса
        self.create_ui()

        # Привязка клавиш управления
        self.root.bind("<Left>", self.rotate_left)
        self.root.bind("<Right>", self.rotate_right)
        self.root.bind("<Up>", self.accelerate)
        self.root.bind("<space>", self.shoot)

    def create_ui(self):
        """Создание и размещение интерфейса жизней, очков и заставки."""
        self.lives_label = tk.Label(
            self.root, text=f"Lives: {self.lives}",
            fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font="TkDefaultFont"
        )
        self.lives_label.pack(anchor="nw", padx=10, pady=10)

        self.score_label = tk.Label(
            self.root, text=f"Score: {self.score}",
            fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font="TkDefaultFont"
        )
        self.score_label.pack(anchor="ne", padx=10, pady=10)

        # Заставка по центру экрана
        self.show_start_screen()

    def show_start_screen(self):
        """Отображение заставки и привязка начала игры к щелчку мыши."""
        self.start_screen = tk.Canvas(
            self.root, width=400, height=200, bg="gray", highlightthickness=0
        )
        self.start_screen.place(relx=0.5, rely=0.5, anchor="center")
        self.start_text = self.start_screen.create_text(
            200, 100, text="Click to Start", fill=TEXT_COLOR, font="TkDefaultFont"
        )

        # Привязка события начала игры
        self.start_screen.bind("<Button-1>", self.start_game)
        self.start_screen.bind("<Escape>", self.end_game)

    def start_game(self, event):
        """Запуск игры по щелчку на заставке."""
        self.start_screen.destroy()
        self.lives = INITIAL_LIVES
        self.score = INITIAL_SCORE
        self.game_mode = "playing"
        self.update_ui()

    def end_game(self, event):
        """Переход в режим окончания игры."""
        self.game_mode = "game_over"
        self.show_start_screen()

    def update_ui(self):
        """Обновление интерфейса жизней и очков."""
        self.lives_label.config(text=f"Lives: {self.lives}")
        self.score_label.config(text=f"Score: {self.score}")

    # Методы для управления кораблем

    def rotate_left(self, event):
        """Поворот корабля влево."""
        if self.game_mode == "playing":
            print("Rotate left")

    def rotate_right(self, event):
        """Поворот корабля вправо."""
        if self.game_mode == "playing":
            print("Rotate right")

    def accelerate(self, event):
        """Ускорение корабля."""
        if self.game_mode == "playing":
            print("Accelerate")

    def shoot(self, event):
        """Выстрел ракетой."""
        if self.game_mode == "playing":
            print("Shoot")


# Запуск игры
if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
