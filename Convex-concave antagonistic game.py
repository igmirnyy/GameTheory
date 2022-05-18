# Найти решение выпукло-вогнутой антагонистической игры в чистых стратегиях
import numpy as np


def f(x, y):
    return -6*x**2 + 16/5*y**2 + 16*x*y + -16/5*x + -48/5*y  # функция определяющая игру


def print_matrix(c, i_colored, j_colored):  # Вывод матрицы с выделенным элементом
    for i in range(len(c)):
        for j in range(len(c[i])):
            if i == i_colored and j == j_colored:
                print("\033[31m\033%6.3f" % c[i][j], end=' ')
            else:
                print("\033[0m\033%6.3f" % c[i][j], end=' ')
        print()


for N in range(2, 11):
    print('N =', N)
    game = np.zeros((N+1, N+1))
    for i in range(N+1):
        for j in range(N+1):
            game[i][j] = f(i/N, j/N)  # формируем матрицу игры
    boo = False
    for i in range(N+1):
        if np.min(game[i, 0:]) == np.max(game[0:, np.argmin(game[i, 0:])]):
            # для всех строк проверяем является ли минимум в строке максимумом в столбце
            i_colored, j_colored = i, np.argmin(game[i, 0:])
            print_matrix(game, i_colored, j_colored)
            print("Есть седловая точка x = %6.3lf, y = %6.3lf, H = %6.3lf" %
                  (i/N, np.argmin(game[i, 0:])/N, np.min(game[i, 0:])))
            boo = True
    if not boo:
        x = np.zeros(N+1, dtype=int)  # хранение выбранных стратегий
        y = np.zeros(N+1, dtype=int)
        strategy_A = 0
        strategy_B = 0  # стратегии первого раунда
        k = 1  # номер раунда
        x[strategy_A] += 1  # Добавляем выбранную стратегию A
        y[strategy_B] += 1  # Добавляем выбранную стратегию B
        sum_A = game[0:, strategy_B]  # возможные выигрыши A при стратегии выбранной B
        sum_B = game[strategy_A, 0:]  # возможные проигрыши B при стратегии выбранной A
        v1 = np.array([np.max(sum_A)])  # массив верхних переделов цены игры
        v2 = np.array([np.min(sum_B)])  # массив нижних пределов цены игры
        eps = np.min(v1) - np.max(v2)  # погрешность
        while eps > 0.1:
            k += 1
            strategy_A = np.argmax(sum_A)  # A выбирает наиболее выгодную стратегию
            strategy_B = np.argmin(sum_B)  # B выбирает наиболее выгодную стратегию
            x[strategy_A] += 1  # Добавляем выбранную стратегию A
            y[strategy_B] += 1  # Добавляем выбранную стратегию B
            sum_A = sum_A + game[0:, strategy_B]  # изменяем возможные выигрыши A учитываю стратегию выбранную B
            sum_B = sum_B + game[strategy_A, 0:]  # изменяем возможные проигрыши B учитываю стратегию выбранную A
            v1 = np.append(v1, np.max(sum_A) / k)  # добавление нового значения верхнего предела цены игры
            v2 = np.append(v2, np.min(sum_B) / k)  # добавление нового значения нижнего предела цены игры
            eps = np.min(v1) - np.max(v2)  # расчет погрешности
        i_colored, j_colored = np.argmax(x), np.argmax(y)
        print_matrix(game, i_colored, j_colored)
        print("Седловой точки нет, решение методом Брауна-Робинсон x = %6.3lf, y = %6.3lf, H = %6.3lf" %
              (np.argmax(x)/N, np.argmax(y)/N, game[np.argmax(x), np.argmax(y)]))
        # Находим смешанное решение и в нем выбираем самый часто встречающийся элемент
