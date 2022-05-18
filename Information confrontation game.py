# Сгенерировать случайную стохастическую матрицу доверия
# Назначить всем агентам случайное начальное мнение. Найти их итоговое мнение
# Случайным образом выбрать агентов влияния первого и второго игрока.
# Смоделировать информационное управление и найти итоговое мнение агентов
import numpy as np


def npstr(arr, is_float):  # массив numpy в строку
    if not is_float:
        return ', '.join(str(x) for x in arr)
    else:
        return ', '.join('{0:7.3}'.format(x) for x in arr)


class Game:
    def __init__(self, lower_bound, higher_bound):
        self.size = 10
        self.eps = 10 ** -6
        self.trust_matrix = self.get_trust_matrix()
        self.limits = (lower_bound, higher_bound)
        self.opinions = np.random.randint(self.limits[0], self.limits[1] + 1, self.size)

    def get_trust_matrix(self):  # Генерация матрицы доверия
        trust_matrix = np.array([])
        for _ in range(self.size):
            row = np.random.randint(0,100,size=10)
            trust_matrix = np.append(trust_matrix, row / np.sum(row))
        return trust_matrix.reshape(10, 10)

    def print_trust_matrix(self,trust_matrix):
        for arr in trust_matrix:
            for i in arr:
                print('{0:7.3}'.format(i), end=' ')
            print()
    def check_accuracy(self, opinions):  # Проверка точности
        return np.count_nonzero(np.abs(self.trust_matrix.dot(opinions) - opinions) < self.eps) != self.size

    def solve_without_player_influence(self):  # Решение в случае отсутствия агентов влияния
        print('Начальные мнения агентов:\nx(0) =', npstr(self.opinions, False))
        iterations = 0
        opinions_without_infl = self.opinions
        trust_matrix = self.trust_matrix
        while self.check_accuracy(opinions_without_infl):
            iterations += 1
            trust_matrix = trust_matrix.dot(self.trust_matrix)
            opinions_without_infl = self.trust_matrix.dot(opinions_without_infl)
        print('Потребовалось %d итераций' % iterations)
        print('Конечные мнения агентов:\nx(inf) =', npstr(opinions_without_infl, True))
        print('Итоговая матрица доверий')
        self.print_trust_matrix(trust_matrix)

    def solve_with_player_influence(self):  # Решение в случае присутствия агентов влияния
        agents = np.random.permutation(self.size)
        u = np.random.randint(1, self.size)
        v = np.random.randint(1, self.size)
        while u + v > self.size:
            u = np.random.randint(1, self.size)
            v = np.random.randint(1, self.size)
        u_agents = agents[:u]
        v_agents = agents[:-v-1:-1]
        print('Агенты первого игрока: %s\nАгенты второго игрока: %s' % (npstr(u_agents, False), npstr(v_agents, False)))
        opinions_with_infl = self.opinions
        u_infl = np.random.randint(0, 50)
        v_infl = -np.random.randint(0, 50)
        print('Мнение агентов первого игрока = %d\nМнение агентов второго игрока = %d' % (u_infl, v_infl))
        for agent in u_agents:
            opinions_with_infl[agent] = u_infl
        for agent in v_agents:
            opinions_with_infl[agent] = v_infl
        print('Начальные мнения агентов с учетом влияния игроков:\nx(0) =', npstr(opinions_with_infl, False))
        iterations = 0
        trust_matrix = self.trust_matrix
        while self.check_accuracy(opinions_with_infl):
            iterations += 1
            trust_matrix = trust_matrix.dot(self.trust_matrix)
            opinions_with_infl = self.trust_matrix.dot(opinions_with_infl)
        print('Потребовалось %d итераций' % iterations)
        print('Конечные мнения агентов с учетом влияния игроков:\nx(inf) =', npstr(opinions_with_infl, True))
        print('Итоговая матрица доверий')
        self.print_trust_matrix(trust_matrix)


game = Game(1, 50)
game.print_trust_matrix(game.trust_matrix)
game.solve_without_player_influence()
game.solve_with_player_influence()
