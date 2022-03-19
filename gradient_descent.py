from decimal import Decimal

class Algo:
    def __init__(self):
        self.e = 0.1
        self.x = [Decimal(1.0), Decimal(1)]
        self.h = Decimal(0.4)

    @staticmethod
    def check_result(x):
        return Decimal(2.8) * x[1] ** 2 + Decimal(1.9) * x[0] + Decimal(2.7) * x[0] ** 2 + Decimal(1.6) - Decimal(1.9) * x[1]

    @staticmethod
    def gradient(x):
        return [Decimal(5.4)*x[0] + Decimal(1.9), Decimal(5.6)* x[1] - Decimal(1.9)]

    def main_loop(self):
        while not self.check_end(self.x):
            new_x = []
            grad = self.gradient(self.x)
            for i in range(len(self.x)):
                new_x.append(self.x[i] - self.h * grad[i])

            if self.check_result(new_x) > self.check_result(self.x):
                self.h /= 2
            else:
                self.x = new_x
            self.report()

    def check_end(self, new_x):
        grad = self.gradient(new_x)
        if (grad[0]**2 + grad[1]**2)**Decimal(0.5) < self.e:
            return True
        else:
            return False

    def report(self):
        print(f"f(x) = {self.check_result(self.x)}\nPoint: {self.x}")


if __name__ == '__main__':
    a = Algo()
    a.main_loop()