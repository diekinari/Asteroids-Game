import tkinter as tk
from PIL import Image, ImageTk
import os
import math
import random

from src.Asteroid import Asteroid
from src.BackgroundAsteroid import BackgroundAsteroid
from src.Ship import Ship
from src.config import *


class Game:
    def __init__(self, root):
        # Инициализация класса Game
        self.start_screen_title = None  # Текст заголовка на стартовом экране
        self.start_screen_clickable = None  # Кликабельный текст на стартовом экране
        self.thrusting = None  # Состояние ускорения корабля (True/False)
        self.rotating_right = None  # Состояние вращения корабля вправо (True/False)
        self.rotating_left = None  # Состояние вращения корабля влево (True/False)

        self.root = root  # Корневой элемент Tkinter
        self.canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="black")
        # Игровое поле с черным фоном
        self.canvas.pack()  # Отображение Canvas на экране

        # Переменные состояния игры
        self.lives = LIVES  # Текущее количество жизней игрока
        self.score = INITIAL_SCORE  # Текущий счет игрока
        self.running = False  # Флаг для определения состояния игры (запущена или остановлена)

        # Элементы пользовательского интерфейса (UI)
        self.heart_images = []  # Список изображений сердец для отображения жизней
        self.heart_widgets = []  # Список виджетов для сердец
        self.background_asteroids = []  # Список астероидов, отображаемых на заднем плане

        self.score_text = self.canvas.create_text(
            10, 10, anchor="nw", fill="white",
            font=("Arial", 16), text=f"Score: {self.score}"
        )  # Текстовое поле для отображения счета в верхнем левом углу

        # Объекты игры
        self.asteroids = []  # Список астероидов на игровом экране
        self.rockets = []  # Список ракет, выпущенных кораблем
        self.ship = None  # Объект корабля

        self.sprites = self.load_sprites()  # Загрузка спрайтов для игры
        self.heart_image = self.sprites["heart"]  # Изображение сердца для отображения жизней
        self.setup_start_screen()  # Настройка стартового экрана

        # Привязка клавиш управления к игровым действиям
        self.root.bind("<KeyPress-Left>", lambda event: self.set_rotation(-1))  # Поворот корабля влево
        self.root.bind("<KeyRelease-Left>", lambda event: self.set_rotation(0))  # Остановка поворота влево
        self.root.bind("<KeyPress-Right>", lambda event: self.set_rotation(1))  # Поворот корабля вправо
        self.root.bind("<KeyRelease-Right>", lambda event: self.set_rotation(0))  # Остановка поворота вправо
        self.root.bind("<KeyPress-Up>", lambda event: self.set_thrust(True))  # Ускорение корабля
        self.root.bind("<KeyRelease-Up>", lambda event: self.set_thrust(False))  # Остановка ускорения
        self.root.bind("<space>", lambda event: self.shoot_rocket())  # Стрельба ракетой

        self.game_over_in_progress = False  # Флаг, указывающий, идет ли обработка экрана окончания игры

    def setup_background_asteroids(self):
        """
        Создает полупрозрачные астероиды для фона стартового экрана.

        Каждый астероид имеет случайные координаты, размер и скорость,
        чтобы создать эффект движущегося звездного поля на фоне.
        """
        for _ in range(10):  # Количество астероидов
            x = random.randint(0, SCREEN_WIDTH)  # Случайная координата X в пределах ширины экрана
            y = random.randint(0, SCREEN_HEIGHT)  # Случайная координата Y в пределах высоты экрана
            size = random.randint(30, 60)  # Случайный размер астероида
            speed = random.uniform(1, 5)  # Случайная скорость астероида
            asteroid = BackgroundAsteroid(self.canvas, x, y, size, speed)
            # Создаем объект астероида и добавляем его в список фоновых астероидов
            self.background_asteroids.append(asteroid)

    def update_background_asteroids(self):
        """
        Обновляет позиции фоновых астероидов.

        Астероиды перемещаются в соответствии со своей скоростью. Если игра еще не началась,
        обновление выполняется циклически с задержкой.
        """
        for asteroid in self.background_asteroids:
            asteroid.update()  # Перемещение астероида

        if not self.running:  # Продолжает обновление, пока игра не началась
            self.root.after(50, self.update_background_asteroids)

    def load_sprites(self):
        """
        Загружает все необходимые спрайты для игры.

        Загружает изображения сердечек и корабля (статического и с работающим двигателем).
        Преобразует их в формат PhotoImage для использования на Canvas.
        """
        sprites = {}

        # Загрузка спрайта сердечка
        heart_path = os.path.join(SPRITE_FOLDER, HEART_IMAGE_FILENAME)
        sprites["heart"] = ImageTk.PhotoImage(
            Image.open(heart_path).resize((HEART_IMAGE_SIZE, HEART_IMAGE_SIZE))
        )

        # Загрузка спрайтов корабля
        static_ship_path = os.path.join(SPRITE_FOLDER, "static_ship.png")
        thrusting_ship_path = os.path.join(SPRITE_FOLDER, "thrusting_ship.png")
        sprites["static_ship"] = ImageTk.PhotoImage(Image.open(static_ship_path))
        sprites["thrusting_ship"] = ImageTk.PhotoImage(Image.open(thrusting_ship_path))

        return sprites

    def update_heart_display(self):
        """
        Обновляет отображение количества жизней в виде сердечек.

        Удаляет старые сердечки и добавляет новые в соответствии с оставшимися жизнями.
        Сердечки размещаются по верхнему правому краю экрана.
        """
        # Удаление текущих виджетов сердечек
        for widget in self.heart_widgets:
            self.canvas.delete(widget)
        self.heart_widgets.clear()

        # Добавление новых сердечек
        for i in range(self.lives):
            x_offset = SCREEN_WIDTH - (i + 1) * (HEART_IMAGE_SIZE + 5) - 10  # Смещение по X
            y_offset = 10  # Фиксированное смещение по Y
            heart = self.canvas.create_image(x_offset, y_offset, anchor="nw", image=self.heart_image)
            self.heart_widgets.append(heart)

        # Убедиться, что сердечки отображаются поверх других элементов
        for heart in self.heart_widgets:
            self.canvas.tag_raise(heart)

    def set_rotation(self, direction):
        """
        Устанавливает направление вращения корабля.

        direction: int
            -1 — вращение влево,
             1 — вращение вправо,
             0 — остановка вращения.
        """
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
        """Устанавливает состояние тяги для корабля.

        Args:
            thrusting (bool): Указывает, включена ли тяга.
        """
        self.thrusting = thrusting

    def start_game(self, event=None):
        """Запускает игру при нажатии на стартовый экран.

        Args:
            event (Optional): Событие, возникающее при нажатии.
        """
        if not self.running:
            self.running = True
            # Удаление элементов стартового экрана
            self.canvas.delete(self.start_screen_title)
            self.canvas.delete(self.start_screen_clickable)

            # Удаление фоновых астероидов
            for asteroid in self.background_asteroids:
                asteroid.remove()

            # Сброс параметров игры и создание корабля
            self.reset_game()
            self.ship = Ship(self.canvas, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.sprites)

            # Генерация астероидов и запуск игрового цикла
            self.spawn_asteroids()
            self.update_game()

    def reset_game(self):
        """Сбрасывает параметры игры до начального состояния."""
        self.lives = LIVES  # Установка количества жизней
        self.score = INITIAL_SCORE  # Установка начального счета
        self.update_heart_display()  # Обновление отображения жизней
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")  # Обновление текста счета

    def setup_start_screen(self):
        """Создает элементы стартового экрана."""
        # Создание фоновых астероидов
        self.setup_background_asteroids()
        self.update_background_asteroids()

        # ASCII-заголовок игры
        ascii_title = """

 █████╗ ███████╗████████╗███████╗██████╗  ██████╗ ██╗██████╗ ███████╗
██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔═══██╗██║██╔══██╗██╔════╝
███████║███████╗   ██║   █████╗  ██████╔╝██║   ██║██║██║  ██║███████╗
██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗██║   ██║██║██║  ██║╚════██║
██║  ██║███████║   ██║   ███████╗██║  ██║╚██████╔╝██║██████╔╝███████║
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═════╝ ╚══════╝

        """
        # Отображение заголовка игры
        self.start_screen_title = self.canvas.create_text(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3,
            fill="cyan", font=("Courier", 14, "bold"),
            text=ascii_title, anchor="center"
        )

        # Текст для начала игры
        self.start_screen_clickable = self.canvas.create_text(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
            fill="white", font=("Arial", 18, "bold"),
            text="Click to Play", anchor="center"
        )
        # Привязка нажатия к запуску игры
        self.canvas.tag_bind(self.start_screen_clickable, "<Button-1>", self.start_game)

        # Обновление отображения жизней
        self.update_heart_display()

    def update_game(self):
        """Основной игровой цикл."""
        if self.running:
            # Обновление состояния корабля
            if self.ship:
                if self.rotating_left:
                    self.ship.rotate(-SHIP_ROTATION_SPEED)
                if self.rotating_right:
                    self.ship.rotate(SHIP_ROTATION_SPEED)

                self.ship.thrusting = self.thrusting
                self.ship.update()

            # Обновление объектов
            self.update_rockets()
            self.update_asteroids()
            self.check_collisions()
            self.cleanup_objects()

            # Генерация дополнительных астероидов
            if not self.game_over_in_progress:
                self.spawn_asteroids()

            # Планирование следующего кадра
            self.root.after(16, self.update_game)

    def cleanup_objects(self):
        """Удаляет объекты, которые больше не нужны."""
        # Удаление устаревших ракет
        for rocket in self.rockets:
            if rocket.expired:
                self.canvas.delete(rocket.sprite_id)
        self.rockets = [r for r in self.rockets if not r.expired]

        # Удаление уничтоженных астероидов
        for asteroid in self.asteroids:
            if asteroid.destroyed and not asteroid.exploding:
                self.canvas.delete(asteroid.sprite_id)
        self.asteroids = [a for a in self.asteroids if not (a.destroyed and not a.exploding)]

    def check_collisions(self):
        """Проверяет столкновения между объектами."""
        # Проверка столкновений ракета-астероид
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
                    self.canvas.tag_raise(self.score_text)
                    break

        # Проверка столкновений корабль-астероид
        if self.ship:
            for asteroid in self.asteroids:
                # Пропускает астероиды, которые ещё взрываются
                if asteroid.exploding:
                    continue

                if self.distance(self.ship.x, self.ship.y, asteroid.x, asteroid.y) < asteroid.radius:
                    print(f"Collision detected: Ship collided with Asteroid {asteroid.sprite_id}")
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
        """Обновляет положение ракет и удаляет истёкшие."""
        for rocket in self.rockets:
            rocket.update()
        # Удаляем ракеты, которые истекли
        self.rockets = [r for r in self.rockets if not r.expired]

    def update_asteroids(self):
        """Обновляет положение астероидов и удаляет завершившие взрыв."""
        for asteroid in self.asteroids:
            asteroid.update()
        # Удаляем астероиды, только если они разрушены и взрыв завершился
        self.asteroids = [a for a in self.asteroids if not (a.destroyed and not a.exploding)]

    def spawn_asteroids(self):
        """Генерирует астероиды, чтобы их общее количество на экране было сбалансированным."""
        if not self.running or self.game_over_in_progress:  # Предотвращение спавна при завершении игры
            return

        # Рассчитываем, сколько астероидов нужно добавить
        num_to_spawn = max(0, MIN_ASTEROIDS - len(self.asteroids))
        for _ in range(num_to_spawn):
            x = random.randint(0, SCREEN_WIDTH)  # Случайная координата x
            y = random.randint(0, SCREEN_HEIGHT)  # Случайная координата y
            dx = random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED)  # Случайная скорость по x
            dy = random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED)  # Случайная скорость по y
            self.asteroids.append(Asteroid(self.canvas, x, y, dx, dy))

        # Ограничиваем общее количество астероидов максимальным значением
        self.asteroids = self.asteroids[:MAX_ASTEROIDS]

    def game_over(self):
        """Обрабатывает завершение игры."""
        print("Game Over! Finalizing animations...")
        self.game_over_in_progress = True  # Indicate game-over sequence is in progress

        # Удаляем корабль с экрана
        if self.ship and hasattr(self.ship, 'sprite_id'):
            self.canvas.delete(self.ship.sprite_id)
            self.ship = None

        # Удаляем все астероиды, кроме "убийцы"
        for asteroid in self.asteroids:
            if not asteroid.exploding:
                self.canvas.delete(asteroid.sprite_id)
        self.asteroids = [a for a in self.asteroids if a.exploding]

        # Удаляем текст счета
        self.canvas.delete(self.score_text)

        # Ждем завершения взрывов перед отображением финального экрана
        self.wait_for_explosions()

    def wait_for_explosions(self):
        """Ждет завершения всех взрывов, прежде чем отобразить финальный экран."""
        explosions_active = any(asteroid.exploding for asteroid in self.asteroids)

        if explosions_active:
            # Если есть активные взрывы, проверяем их через короткий интервал
            self.root.after(100, self.wait_for_explosions)
        else:
            # Когда взрывы завершены, отображаем финальный экран
            self.finalize_game_over()

    def finalize_game_over(self):
        """Очищает экран и отображает финальное сообщение 'Game Over'."""
        # Удаляем все оставшиеся элементы игры
        for asteroid in self.asteroids:
            if hasattr(asteroid, 'sprite_id'):
                self.canvas.delete(asteroid.sprite_id)
        self.asteroids.clear()

        for rocket in self.rockets:
            if hasattr(rocket, 'sprite_id'):
                self.canvas.delete(rocket.sprite_id)
        self.rockets.clear()

        # ASCII-арт с сообщением "Game Over"
        game_over_ascii = """
          _____                         ____                 
         / ____|                       / __ \                
        | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ 
        | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|
        | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   
         \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   
        """
        self.canvas.create_text(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 - 50,
                                fill="red", font=("Courier", 16, "bold"),
                                text=game_over_ascii, anchor="center")

        # Отображаем финальный счет
        self.canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                                fill="white", font=("Arial", 18, "bold"),
                                text=f"Final Score: {self.score}", anchor="center")

        # Завершаем игру
        self.running = False
        print("Game Over sequence completed.")

    def shoot_rocket(self):
        """Выстреливает ракету из корабля."""
        if self.running:
            self.rockets.append(self.ship.shoot())

    @staticmethod
    def distance(x1, y1, x2, y2):
        """Вычисляет расстояние между двумя точками."""
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
