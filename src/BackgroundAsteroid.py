from PIL import Image, ImageTk
import os

from src.config import *


class BackgroundAsteroid:
    """
    Класс BackgroundAsteroid представляет декоративный астероид на фоне заставки игры.

    Атрибуты:
        canvas (Canvas): Холст, на котором отрисовывается астероид.
        x (float): Координата x текущего положения астероида.
        y (float): Координата y текущего положения астероида.
        size (int): Размер астероида (ширина и высота в пикселях).
        speed (float): Скорость перемещения астероида по экрану.
        image (ImageTk.PhotoImage): Текущее изображение астероида.
        sprite_id (int): Идентификатор спрайта астероида на холсте.
    """

    def __init__(self, canvas, x, y, size, speed):
        """
        Инициализация объекта BackgroundAsteroid.

        Аргументы:
            canvas (Canvas): Холст, на котором будет отображаться астероид.
            x (float): Начальная координата x.
            y (float): Начальная координата y.
            size (int): Размер астероида в пикселях.
            speed (float): Скорость движения астероида по экрану.
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed

        # Загружаем изображение астероида и изменяем его размер
        self.image = ImageTk.PhotoImage(
            Image.open(os.path.join(SPRITE_FOLDER, "asteroid_old.png")).resize(
                (self.size, self.size), Image.Resampling.LANCZOS
            )
        )

        # Создаем спрайт астероида на холсте
        self.sprite_id = self.canvas.create_image(self.x, self.y, image=self.image)

    def update(self):
        """
        Обновляет положение астероида, перемещая его влево.

        Если астероид выходит за пределы экрана, он возвращается с правой стороны.
        """
        self.x -= self.speed
        if self.x < -self.size:  # Проверяем выход за левую границу экрана
            self.x = SCREEN_WIDTH + self.size
        self.canvas.coords(self.sprite_id, self.x, self.y)

    def remove(self):
        """
        Удаляет спрайт астероида с холста.
        """
        self.canvas.delete(self.sprite_id)

