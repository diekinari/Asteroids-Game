# Константы для игры Asteroids

SCREEN_WIDTH = 800  # Ширина игрового экрана в пикселях
SCREEN_HEIGHT = 600  # Высота игрового экрана в пикселях
LIVES = 3  # Начальное количество жизней игрока
INITIAL_SCORE = 0  # Начальное количество очков игрока
ASTEROID_SPEED = 2  # Скорость движения астероидов (чем выше, тем быстрее)
SHIP_THRUST = 0.1  # Ускорение корабля при движении вперед
SHIP_ROTATION_SPEED = 3  # Скорость вращения корабля (градусы за кадр)
ROCKET_SPEED = 8  # Скорость ракеты (пиксели за кадр)
ROCKET_LIFETIME = 50  # Время жизни ракеты (в кадрах)
MIN_ASTEROIDS = 5  # Минимальное количество астероидов на экране
MAX_ASTEROIDS = 10  # Максимальное количество астероидов на экране

SPRITE_FOLDER = "public"  # Папка, где хранятся файлы спрайтов
HEART_IMAGE_SIZE = 32  # Размер изображения сердца (пиксели)
HEART_IMAGE_FILENAME = f"heart pixel art {HEART_IMAGE_SIZE}x{HEART_IMAGE_SIZE}.png"  # Имя файла изображения сердца
STATIC_SHIP_SPRITE = "static_ship.png"  # Имя файла спрайта корабля в статическом состоянии
THRUSTING_SHIP_SPRITE = "thrusting_ship.png"  # Имя файла спрайта корабля при ускорении
