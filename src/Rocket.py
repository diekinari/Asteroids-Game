import math
from PIL import Image, ImageTk
import os
from src.config import *


class Rocket:
    """
    Класс Rocket представляет ракету, которая движется в заданном направлении
    с ограниченным временем жизни.

    Атрибуты:
        canvas (Canvas): Холст для отображения ракеты.
        x (float): Текущая координата x ракеты.
        y (float): Текущая координата y ракеты.
        angle (float): Угол направления движения ракеты в градусах.
        velocity_x (float): Скорость ракеты по оси x.
        velocity_y (float): Скорость ракеты по оси y.
        lifetime (int): Время жизни ракеты в кадрах.
        expired (bool): Флаг, указывающий, истекло ли время жизни ракеты.
        image (ImageTk.PhotoImage): Изображение ракеты.
        sprite_id (int): Идентификатор спрайта ракеты на холсте.
    """

    def __init__(self, canvas, x, y, angle):
        """
        Инициализация объекта Rocket.

        Аргументы:
            canvas (Canvas): Холст для отрисовки ракеты.
            x (float): Начальная координата x.
            y (float): Начальная координата y.
            angle (float): Угол движения ракеты в градусах.
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.angle = angle
        self.velocity_x = ROCKET_SPEED * math.cos(math.radians(angle))
        self.velocity_y = ROCKET_SPEED * math.sin(math.radians(angle))
        self.lifetime = ROCKET_LIFETIME
        self.expired = False

        # Загрузка и вращение изображения ракеты
        original_rocket_image = Image.open(os.path.join(SPRITE_FOLDER, "rocket.png"))
        rotated_image = original_rocket_image.rotate(angle)
        self.image = ImageTk.PhotoImage(rotated_image)

        # Создание спрайта на холсте
        self.sprite_id = self.canvas.create_image(self.x, self.y, image=self.image)

    def update(self):
        """
        Обновляет положение ракеты, проверяет её время жизни и удаляет с холста, если срок истёк.
        """
        # Обновление позиции с учётом границ экрана
        self.x = (self.x + self.velocity_x) % SCREEN_WIDTH
        self.y = (self.y + self.velocity_y) % SCREEN_HEIGHT
        self.canvas.coords(self.sprite_id, self.x, self.y)

        # Уменьшение времени жизни
        self.lifetime -= 1

        # Проверка истечения времени жизни
        if self.lifetime <= 0:
            self.expired = True
            self.canvas.delete(self.sprite_id)

