# Для случайно сгенерированной биматричной игры, а также игр 'Перекресток', 'Семейный спор', 'Дилемма Заключенного'
# найти ситуации оптимальные по Парето, равновесные по Нэшу и пересечения этих множеств
import numpy as np


def is_nash(game, i, j):  # проверка элемента на равновесие по Нэшу
    if game[i, j, 0] == np.max(game[0:, j, 0]) and game[i, j, 1] == np.max(game[i, 0:, 1]):
        return 1
    else:
        return 0


def is_pareto(game, i, j):  # проверка элемента на оптимальность по Парето
    for x in range(len(game)):
        for y in range(len(game)):
            if (game[x, y, 0] > game[i, j, 0] and game[x, y, 1] >= game[i, j, 1])\
                    or (game[x, y, 1] > game[i, j, 1] and game[x, y, 0] >= game[i, j, 0]):
                return 0
    return 1


def pareto_nash(game):  # поиск элементов оптимальных по Парето и/или равновесных по Нэшу
    pareto = []  # Оптимальные по Парето
    nash = []  # Равновесные по Нэшу
    for i in range(len(game)):
        for j in range(len(game[i])):
            if is_nash(game, i, j):
                nash += [(game[i, j, 0], game[i, j, 1])]
            if is_pareto(game, i, j):
                pareto += [(game[i, j, 0], game[i, j, 1])]
    for i in range(len(game)):
        for j in range(len(game[i])):
            t = (game[i, j, 0], game[i, j, 1])
            if (t in pareto) and (t in nash):
                print("\033[31m\033(%3d,%3d)" % (t[0], t[1]), end=' ')
                # вывод оптимальных по Парето и равновесных по Нэшу красным
            elif t in pareto:
                print("\033[32m\033(%3d,%3d)" % (t[0], t[1]), end=' ')  # вывод оптимальных по Парето зеленым
            elif t in nash:
                print("\033[35m\033(%3d,%3d)" % (t[0], t[1]), end=' ')  # вывод оптимальных по Парето фиолетовым
            else:
                print("\033[0m\033(%3d,%3d)" % (t[0], t[1]), end=' ')  # вывод остальных белым
        print()
    print("\033[0m\033")
    print("Оптимальные по Парето:", end=' ')
    for i in pareto:
        print(i, end=' ')
    print("\nРавновесные по Нэшу:", end=' ')
    for i in nash:
        print(i, end=' ')
    print("\nОптимальные по Парето и Равновесные по Нэшу:", end=' ')
    for i in nash:
        if i in pareto:
            print(i, end=' ')


print("Перекресток")
game = np.array([[[1, 1], [1, 2]], [[2, 1], [0, 0]]])
pareto_nash(game)
print("\nСемейный спор")
game = np.array([[[4, 1], [0, 0]], [[0, 0], [1, 4]]])
pareto_nash(game)
print("\nДилемма заключенного")
game = np.array([[[-5, -5], [0, - 10]], [[-10, 0], [-1, -1]]])
pareto_nash(game)
print('\nСгенерированная игра')
game = np.random.randint(-50, 50, (10, 10, 2))
pareto_nash(game)
