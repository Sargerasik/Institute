"""
2,8 * x2^2 + 1.9 * x1 + 2,7 *x1^2 + 1,6 - 1,9*x2
"""
import random
class Algo:
    def start_base_point(self):
        """
        установка базисной точки

        :param x: базисная точка
        :param h: Шаг по координатным направлениям
        :param d: коэфициент уменьшения шага
        :return:
        """
        self.x = [1, 1]
        self.h = 0.2
        self.d = 2
        self.e = 0.1
        self.result = self.check_result(self.x)

    @staticmethod
    def check_result(x):
        return 2.8 * x[1] ** 2 + 1.9 * x[0] + 2.7 * x[0] ** 2 + 1.6 - 1.9 * x[1]

    def steps(self, index: int):
        """
        Проверка окрестности точки x[index] в положительно и отрицательном направление
        :param index:
        :return:
        """
        successful = False
        x_copy = self.x.copy()
        x_copy[index] = x_copy[index] + self.h
        if self.check_result(x_copy) < self.result:
            self.x = x_copy.copy()
            successful = True

        x_copy = self.x.copy()
        x_copy[index] = x_copy[index] - self.h
        if self.check_result(x_copy) < self.result:
            self.x = x_copy.copy()
            successful = True


    def search(self):

        for i in range(len(self.x)):
            self.steps(i)




    