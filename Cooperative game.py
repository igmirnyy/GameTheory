# Проверить кооперативную игру на выпуклость и супераддитивность
# Рассчитать вектор Шепли
# Проверить выполнение условий групповой и индивидуальной рационализации
import numpy as np
from math import factorial as fact


class Game:
    def __init__(self, game_coals: dict):
        self.game = game_coals  # словарь в котором коалиции сопоставлен выигрыш

    def all_coalitions(self):  # перечисление всех коалиций игры
        return [set(map(int, k.split(','))) for k in self.game.keys() if k != '']

    def is_superadditive(self):  # проверка игры на супераддитивность
        coalitions = self.all_coalitions()
        superadditive = True
        errors = []
        for i in range(len(coalitions)):
            for j in range(i, len(coalitions)):
                if len(coalitions[i] & coalitions[j]) == 0:  # если пересечение коалиций пустое
                    st = ','.join(map(str, sorted(list(coalitions[i] | coalitions[j]))))  # объединение коалиций
                    s = ','.join(map(str, sorted(list(coalitions[i]))))  # первая коалиция
                    t = ','.join(map(str, sorted(list(coalitions[j]))))  # вторая коалиция
                    if self.game[st] < self.game[s] + self.game[t]:  # проверка условия супер аддитивности
                        superadditive = False
                        if st not in errors:
                            errors.append(st)  # сохранение коалиций для которых условие не выполняется
        return superadditive, errors

    def make_superadditive(self):  # изменение игры для того чтобы она стала супераддитивной
        superadditive, errors = self.is_superadditive()
        while not superadditive:
            for error in errors:
                self.game[error] += 1
            superadditive, errors = self.is_superadditive()

    def is_convex(self): # проверка игры на выпуклость
        coalitions = self.all_coalitions()
        for i in range(len(coalitions)):
            for j in range(i, len(coalitions)):
                s_cup_t = ','.join(map(str, sorted(list(coalitions[i] | coalitions[j]))))  # объединение коалиций
                s_cap_t = ','.join(map(str, sorted(list(coalitions[i] & coalitions[j]))))  # пересечение коалиций
                s = ','.join(map(str, sorted(list(coalitions[i]))))  # первая коалиция
                t = ','.join(map(str, sorted(list(coalitions[j]))))  # вторая коалиция
                if self.game[s_cup_t] + self.game[s_cap_t] < self.game[s] + self.game[t]:  # проверка условия выпуклости
                    return False
        return True

    def shepli_vector(self):  # получение вектора Шепли
        vector = np.array([0, 0, 0, 0])
        coalitions = self.all_coalitions()
        for p in range(1, 5):  # игрок
            for coal in coalitions:  # коалиция
                player = set()
                player.add(p)
                if len(player & coal) == 0:  # если игрок не в коалиции переход к следующей коалиции
                    continue
                else:
                    v_s = ','.join(map(str, sorted(list(coal))))   # коалиция
                    v_s_i = ','.join(map(str, sorted(list(coal - player))))  # коалиция без игрока
                    vector[p-1] += fact(len(coal) - 1) * fact(4 - len(coal)) * (self.game[v_s] - self.game[v_s_i])
        return vector / fact(4)

    def __str__(self):  # преобразования игры к строке
        game_str = 'Игра:\nv({Ø}) = 0;'
        game_str += ';\n'.join(['v({{{0}}}) = {1}'.format(k, v) for k, v in self.game.items()])[10:]
        return game_str

    def is_group_rational(self):  # проверка вектора Шепли на групповую рациональность
        vector = self.shepli_vector()
        if np.sum(vector) == self.game['1,2,3,4']:
            return True
        else:
            return False

    def is_individually_rational(self):  # проверка вектора Шепли на индивидуальную рациональность
        vector = self.shepli_vector()
        for player in range(1,5):
            if vector[player - 1] < self.game[str(player)]:
                return False
        return True

    def solve(self):
        superadditive, errors = self.is_superadditive()
        if superadditive:
            print("Игра является супераддитивной")
        else:
            print("Игра не является супераддитивной")
            self.make_superadditive()
            print('Измененная игра', game)
        if self.is_convex():
            print("Игра является выпуклой")
        else:
            print("Игра не является выпуклой")
        vector = self.shepli_vector()
        print('Вектор Шепли:', *vector, sep=' ')
        if self.is_group_rational():
            print('Условия групповой рационализации выполнены')
        if self.is_individually_rational():
            print('Условия групповой рационализации выполнены')


game_coals = {
    '': 0,
    '1': 4,
    '2': 1,
    '3': 1,
    '4': 1,
    '1,2': 7,
    '1,3': 7,
    '1,4': 7,
    '2,3': 3,
    '2,4': 2,
    '3,4': 2,
    '1,2,3': 10,
    '1,2,4': 10,
    '1,3,4': 10,
    '2,3,4': 6,
    '1,2,3,4': 12
}
game = Game(game_coals)
game.solve()
