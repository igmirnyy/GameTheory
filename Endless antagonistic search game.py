# Найти решение бесконечной антагонистической игры поиска на конусе
import numpy as np
import math
import matplotlib.pyplot as plt
import random


class Cone:  # Конус
    def __init__(self, radius, height):
        self.a = 1
        self.b = 1
        self.c = radius / height
        self.radius = radius
        self.bot = - (2 * radius * height)/(2 * radius + (4 * height * height + 4 * radius * radius) ** 0.5)
        self.height = height + self.bot

    def get_inscribed_sphere(self, dots_num):  # точки распределенные на вписанной сфере по Фибоначчи
        golden_ratio = (1 + 5 ** 0.5) / 2
        i = np.arange(0, dots_num)
        theta = 2 * np.pi * i / golden_ratio
        phi = np.arccos(1 - 2 * (i + 0.5) / dots_num)
        x, y, z = np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)
        return np.column_stack([-self.bot * x, -self.bot * y, -self.bot * z])

    def project_point_to_base(self, x, y, z):  # Проекция точки на основание
        k = self.bot / z
        return np.array([k * x, k * y, k * z, 0.5])

    def project_point_to_cone(self, x, y, z):  # Проекция точки на всю поверхность конуса

        a1 = x**2/(self.a**2) + y**2/(self.b**2) - z**2/(self.c**2)
        a2 = 2 * self.height * z / (self.c ** 2)
        a3 = -((self.height/self.c) ** 2)
        det = a2 ** 2 - 4 * a1 * a3
        if det < 0:
            return self.project_point_to_base(x, y, z)
        else:
            k1, k2 = (-a2 - math.sqrt(det))/(2 * a1), (-a2 + math.sqrt(det))/(2 * a1)
            if k1 > 0 and k2 > 0:
                k = min(k1, k2)
            else:
                k = max(k1, k2)
        if k * z < self.bot or k < 0:

            return self.project_point_to_base(x, y, z)
        else:
            if y <= x:
                return np.array([k * x, k * y, k * z, 0.8])
            else:
                return np.array([k * x, k * y, k * z, 0.3])

    def get_random_point(self):  # Случайная точка на конусе
        theta = random.random() * 2 * np.pi
        phi = random.random() * np.pi
        x, y, z = math.cos(theta) * math.sin(phi), math.sin(theta) * math.sin(phi), math.cos(phi)
        x = -self.bot * x
        y = -self.bot * y
        z = -self.bot * z
        return self.project_point_to_cone(x, y, z)


def check_distance(point1, point2, search_rad):  # расстояние между двумя точками
    return (search_rad**2) >= (np.sum((point1-point2)**2))


# Инициализация фигуры

radius = float(input('Enter cone\'s radius: '))
height = float(input('Enter cone\'s height: '))
dots = int(input('Enter amount of dots randomly splitted on the cone: '))
search_rad = float(input('Enter search radius: '))
attempts = int(input('Enter amount of search attempts: '))

Cone = Cone(radius, height)

# Инициализация графика
fig = plt.figure(figsize=(4, 8))
ax = fig.add_subplot(211, projection='3d')
bx = fig.add_subplot(212, projection='3d')

# Рисовка конуса
Z = np.linspace(0, height, 40)
t = np.linspace(0, 2*np.pi, 100)
for value in Z:  # Боковая поверхность
    x = value * np.cos(t) * Cone.a / Cone.c
    y = value * np.sin(t) * Cone.b / Cone.c
    bx.plot(x, y, Cone.height - value, '-', color='#AEA04B', alpha=0.3)
    ax.plot(x, y, Cone.height - value, '-', color='#AEA04B', alpha=0.3)
rads = np.linspace(0, Cone.radius, 100)
for rad in rads:  # Основание
    x = rad * np.cos(t)
    y = rad * np.sin(t)
    bx.plot(x, y, Cone.bot, '-', color='#AEA04B', alpha=0.3)
    ax.plot(x, y, Cone.bot, '-', color='#AEA04B', alpha=0.3)


# Создание точек расположенных изначально
points = []
for i in range(dots):
    points.append(Cone.get_random_point())
    bx.scatter(*points[-1][:3], alpha=points[-1][3]/2, c='m')
    ax.scatter(*points[-1][:3], alpha=points[-1][3], c='m')

# Создание точек угадывающего
sphere = Cone.get_inscribed_sphere(attempts)
guesses = []
for point in sphere:
    projection = Cone.project_point_to_cone(point[0], point[1], point[2])
    guesses.append(projection)
guesses = np.array(guesses)

# Решение игры
wins = 0
for i in range(attempts):
    guess = guesses[i]
    flag = False
    for point in points:
        if check_distance(guess[:3], point[:3], search_rad):
            flag = True
            break
    if flag:
        wins += 1
        bx.scatter(*guess[:3], c='g', alpha=guess[3])
    else:
        bx.scatter(*guess[:3], c='r', alpha=guess[3])
print('Game\'s value', wins/attempts)
fig.tight_layout()

plt.show()
