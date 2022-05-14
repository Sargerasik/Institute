"""
2,8 * x2^2 + 1.9 * x1 + 2,7 *x1^2 + 1,6 - 1,9*x2
"""


class Algo:
    def __init__(self):
        """
        установка базисной точки

        :param x: базисная точка
        :param h: Шаг по координатным направлениям
        :param d: коэфициент уменьшения шага
        :return: None
        """
        self.m = 2
        self.old_x = None
        self.x = [10, 10]
        self.h = 0.2
        self.d = 2
        self.e = 0.000001

    @staticmethod
    def check_result(x):
        """
        Проверяет результат функции при переданных параметрах

        :param x: Параметры функции
        :return: Результат функции
        """
        return 2.8 * x[1] ** 2 + 1.9 * x[0] + 2.7 * x[0] ** 2 + 1.6 - 1.9 * x[1]

    def steps(self, index: int):
        """
        Проверка окрестности точки x[index] в положительно и отрицательном направление
        :param index:
        :return:
        """
        x_copy = self.x.copy()
        x_copy[index] = x_copy[index] + self.h
        if self.check_result(x_copy) < self.check_result(self.x):
            self.x = x_copy.copy()

        x_copy = self.x.copy()
        x_copy[index] = x_copy[index] - self.h
        if self.check_result(x_copy) < self.check_result(self.x):
            self.x = x_copy.copy()

    def search(self):
        """
        Реализует поиск следующего решения.
        :return:
        """
        old_res = self.check_result(self.x)
        self.old_x = self.x
        for i in range(len(self.x)):
            self.steps(i)
        new_res = self.check_result(self.x)

        if new_res < old_res:
            self.template()
        else:
            self.h /= 2

    def template(self):
        """
        Реализует поиск по шаблону

        :return:
        """
        temp_x = []
        for i in range(len(self.x)):
            temp_x.append(self.x[i] + self.m * (self.x[i] - self.old_x[i]))

        if self.check_result(temp_x) < self.check_result(self.x):
            self.x = temp_x
        else:
            self.h /= 2
            self.search()

    def __str__(self):
        return f"f(x) = {self.check_result(self.x)}\nPoint: {self.x}\n"


def main():
    """
    Основной цикл. Закончится в том случае, когда значение шага будет меньше или равно эпсиланту
    :return:
    """
    a = Algo()
    while a.h >= a.e:
        a.search()
        print(a)

if __name__ == '__main__':
    main()
