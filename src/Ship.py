import math
from PIL import Image, ImageTk
import os

from src.Rocket import Rocket
from src.config import *


class Ship:
    """
    Класс Ship представляет космический корабль игрока.

    Атрибуты:
        canvas (Canvas): Холст, на котором отрисовывается корабль.
        x (float): Координата x текущего положения корабля.
        y (float): Координата y текущего положения корабля.
        angle (float): Угол поворота корабля (в градусах).
        radius (float): Радиус корабля для вычислений.
        velocity_x (float): Горизонтальная скорость корабля.
        velocity_y (float): Вертикальная скорость корабля.
        thrusting (bool): Указывает, включен ли режим тяги.
        sprites (dict): Словарь с графическими ресурсами для спрайтов.
        original_static_ship (PIL.Image): Изображение неподвижного корабля.
        original_thrusting_ship (PIL.Image): Изображение корабля с включенной тягой.
        current_image (ImageTk.PhotoImage): Текущее изображение корабля для отображения.
        sprite_id (int): Идентификатор спрайта на холсте (создается динамически).
    """

    def __init__(self, canvas, x, y, sprites):
        """
        Инициализация объекта Ship.

        Аргументы:
            canvas (Canvas): Холст, на котором будет отображаться корабль.
            x (float): Начальная координата x.
            y (float): Начальная координата y.
            sprites (dict): Словарь с графическими ресурсами для корабля.
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.angle = 270  # Угол поворота, изначально направлен вверх.
        self.radius = 30
        self.velocity_x = 0
        self.velocity_y = 0
        self.thrusting = False
        self.sprites = sprites
        # Загружаем изображения корабля
        self.original_static_ship = Image.open(os.path.join(SPRITE_FOLDER, "new_static_ship.png")).resize(
            (60, 60), Image.Resampling.LANCZOS
        )
        self.original_thrusting_ship = Image.open(os.path.join(SPRITE_FOLDER, "new_thrusting_ship.png")).resize(
            (60, 60), Image.Resampling.LANCZOS
        )
        self.current_image = None
        self.update_image()  # Устанавливаем начальный спрайт

    def update_image(self):
        """
        Обновляет изображение корабля в зависимости от угла поворота и режима тяги.
        """
        sprite_to_use = (
            self.original_thrusting_ship if self.thrusting else self.original_static_ship
        )
        rotated_image = sprite_to_use.rotate(-(self.angle - 90), resample=Image.BICUBIC)  # Корректируем угол
        self.current_image = ImageTk.PhotoImage(rotated_image)
        if hasattr(self, 'sprite_id'):
            self.canvas.itemconfig(self.sprite_id, image=self.current_image)
        else:
            self.sprite_id = self.canvas.create_image(self.x, self.y, image=self.current_image)

    def update(self):
        """
        Обновляет состояние корабля: применяет тягу, трение и изменяет координаты.
        """
        if self.thrusting:
            # Применяем ускорение в направлении корабля
            self.velocity_x += SHIP_THRUST * math.cos(math.radians(self.angle))
            self.velocity_y += SHIP_THRUST * math.sin(math.radians(self.angle))
        else:
            # Применяем трение для снижения скорости
            self.velocity_x *= 0.99
            self.velocity_y *= 0.99

        # Обновляем координаты с учетом циклической границы экрана
        self.x = (self.x + self.velocity_x) % SCREEN_WIDTH
        self.y = (self.y + self.velocity_y) % SCREEN_HEIGHT

        self.update_image()  # Обновляем изображение корабля
        self.canvas.coords(self.sprite_id, self.x, self.y)

    def rotate(self, angle):
        """
        Поворачивает корабль на заданный угол.

        Аргументы:
            angle (float): Угол в градусах, на который нужно повернуть корабль.
        """
        self.angle = (self.angle + angle) % 360

    def shoot(self):
        """
        Выпускает ракету из носа корабля.

        Возвращает:
            Rocket: Объект ракеты, выпущенной из корабля.
        """
        # Вычисляем координаты носа корабля
        nose_x = self.x + self.radius * math.cos(math.radians(self.angle))
        nose_y = self.y + self.radius * math.sin(math.radians(self.angle))
        return Rocket(self.canvas, nose_x, nose_y, self.angle)

    def respawn(self):
        """
        Возвращает корабль в центр экрана с обнулением скорости.
        """
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.velocity_x = 0
        self.velocity_y = 0
