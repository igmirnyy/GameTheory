# Используя метод обратной индукции найти решение конечной позиционной игры
import numpy as np


class TreeNode:  # Корень дерева
    def __init__(self, values):
        self.values = values  # Массив выигрышей
        self.left = None  # Левый корень
        self.mid = None  # Центральный корень
        self.right = None  # Правый корень


def form_binary_tree(depth):  # Создание дерева
    if depth == 6:
        return None  # При глубине 6 заканчиваем формирование дерева
    if depth == 5:
        tree = TreeNode(np.random.randint(-20, 15+1, 3))  # В последнем уровне заполняем массивы выигрышей
    else:
        tree = TreeNode(None)  # Не последние вершины не заполняем
    if depth % 3 != 1:  # Вершины с 2 стратегиями
        tree.left = form_binary_tree(depth+1)
        tree.right = form_binary_tree(depth+1)
    else:  # Вершины с 3 стратегиями
        tree.left = form_binary_tree(depth + 1)
        tree.mid = form_binary_tree(depth + 1)
        tree.right = form_binary_tree(depth + 1)
    return tree


def print_binary_tree(node, depth):  # Вывод бинарного дерева слева направо
    if node:
        print_binary_tree(node.left, depth + 1)
        print_binary_tree(node.mid, depth + 1)
        print_binary_tree(node.right, depth + 1)
        print(node.values, depth)


def choose(node, depth):  # Выбор стратегии
    player = depth % 3  # Номер игрока совершающего ход
    ret = []
    if player == 1:  # Игрок у которого выбор из 3 вершин большей глубины
        arr = np.hstack([node.left.values.reshape(1, -1), node.mid.values.reshape(1, -1), node.right.values.reshape(1, -1)]).reshape(-1, 3)
# Все массивы преобразовываем в одномерные, соединяем их и переформируем в массив m*3
    else:  # Игроки у которого выбор из 2 вершин большей глубины
        arr = np.hstack([node.left.values.reshape(1, -1), node.right.values.reshape(1, -1)]).reshape(-1, 3)
# Все массивы преобразовываем в одномерные, соединяем их и переформируем в массив m*3
    for i in arr:
        if np.max(arr[0:, player]) == i[player]:  # Ищем все наиболее выгодные стратегии
            ret += [i]
    return np.array(ret)  # Возвращаем наиболее выгодные стратегии


def foo(node, depth):  # Заполнение дерева
    if depth < 4:
        foo(node.left, depth + 1)  # Заполняем следующую левую вершину
        if depth % 3 == 1:  # Если у вершины три корня
            foo(node.mid, depth + 1)  # Заполняем следующую центральную вершину
        foo(node.right, depth + 1)  # Заполняем следующую правую вершину
    node.values = choose(node, depth)  # Заполняем наиболее выгодной стратегией


tree = form_binary_tree(0)
foo(tree, 0)
print_binary_tree(tree, 0)
for i in range(len(tree.values)):
    print("(%3d, %3d, %3d)" % (tree.values[i][0], tree.values[i][1], tree.values[i][2]))
# print_binary_tree(tree, 0)
