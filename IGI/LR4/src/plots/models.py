"""models"""

import math
import statistics
import matplotlib.pyplot as plt


class Report:
    """series report"""

    def __init__(self):
        self.x: list[float] = []
        self.n: list[int] = []
        self.res: list[float] = []
        self.math_res: list[float] = []
        self.eps: float
        self.mean: float
        self.median: float
        self.mode: float
        self.variance: float
        self.stdev: float

    def plot(self):
        """plot matplotlib"""
        plt.title("Func graph")

        plt.plot(self.x, self.res)
        plt.plot(self.x, self.math_res)

        plt.title("Function Comparison: Series vs Exact", fontsize=14)
        plt.xlabel("x", fontsize=12)
        plt.ylabel("f(x)", fontsize=12)
        plt.legend(["Series", "Func"])


        plt.grid(True, linestyle=':', alpha=0.7, color='gray')

        if len(self.x) > 0 and len(self.res) > 0:
            plt.text(self.x[0], self.res[-1],
                     r"$\ln{\frac{x+1}{x-1}}$", fontsize=14)

        plt.savefig('plot.png')

    def __str__(self):
        """report string"""
        res_str = f"Mean: {self.mean:.5}\n" \
            f"Median: {self.median:.5}\n" \
            f"Mode: {self.mode:.5}\n" \
            f"Variance: {self.variance:.5}\n" \
            f"Standard deviation: {self.stdev:.5}\n"
        column_width = 10
        table = f"{'x':^{column_width}}|{'n':^{column_width}}|{'F(x)':^{column_width}}|" + \
            f"{'Math F(x)':^{column_width}}|{'eps':^{column_width}}\n"
        table += (len(table) - 1) * '-' + '\n'
        for x, n, res, math_res in zip(self.x, self.n, self.res, self.math_res):
            table += f"{x:^{column_width}.5}|{n:^{column_width}}|{res:^{column_width}.5}|" + \
                f"{math_res:^{column_width}.5}|{self.eps:^{column_width}.5}\n"
        return res_str + table


class Calculator:
    """series calculator"""

    def __init__(self):
        self._report = None

    def _f(self, x: float, eps: float = 0.001) -> tuple[float, int]:
        """Calculates ln((x + 1) / (x - 1)) via serias expansion

        Args:
            x (float): Function argument
            eps (float, optional): Precision. Defaults to 0.001.


            tuple[float, int]: Result and num of executed iterations
        """
        def member(n):
            try:
                return math.pow((2 * n + 1) * math.pow(x, 2 * n + 1), -1)
            except ValueError:
                return 0

        max_i = 500
        res = 0
        i = 0
        for i in range(max_i):
            if math.fabs(member(i) - member(i - 1)) < eps:
                break
            res += member(i)

        return 2 * res, i

    def calculate(self, x_min: float, x_max: float, step: float, eps: float):
        """calculate series"""
        self._report = Report()
        self._report.eps = eps
        x = x_min
        while x <= x_max:
            self._report.x.append(x)
            res, n = self._f(
                x, eps)
            self._report.res.append(res)
            self._report.n.append(n)
            self._report.math_res.append(math.log((x + 1) / (x - 1)))
            x += step

        seq = self._report.res

        self._report.mean = statistics.mean(seq)
        self._report.median = statistics.median(seq)
        self._report.mode = statistics.mode(seq)
        self._report.variance = statistics.variance(seq)
        self._report.stdev = statistics.stdev(seq)

    @property
    def report(self) -> Report:
        """report getter"""
        return self._report
