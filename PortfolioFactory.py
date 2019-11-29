import Portfolio
import numpy as np

class PortfolioFactory:

    @staticmethod
    def get_available_portfolios():
        means = [0.06, 0.059, 0.07, 0.056, 0.019, 0.052, 0.015]
        standard_deviations = [0.091, 0.202, 0.268, 0.207, 0.038, 0.07, 0.058]
        cor = np.array([[1.000, 0.740, 0.670, 0.740, 0.130, 0.470, 0.020],
                        [0.740, 1.000, 0.700, 0.780, 0.090, 0.460, 0.000],
                        [0.670, 0.700, 1.000, 0.660, 0.070, 0.450, -0.03],
                        [0.740, 0.780, 0.660, 1.000, 0.100, 0.370, -0.03],
                        [0.130, 0.090, 0.070, 0.100, 1.000, 0.100, 0.100],
                        [0.470, 0.460, 0.450, 0.370, 0.100, 1.000, 0.550],
                        [0.020, 0.000, -0.03, -0.03, 0.100, 0.550, 1.000]])

        weights1 = [0.3, 0.3, 0.1, 0.1, 0.1, 0.1, 0]
        fees1 = 0.2

        weights2 = [0.3, 0.3, 0.1, 0.1, 0.1, 0.1, 0]
        fees2 = 0.2

        weights3 = [0.3, 0.3, 0.1, 0.1, 0.1, 0.1, 0]
        fees3 = 0.2

        portfolios = [
            Portfolio.Portfolio(
                weights = weights1,
                means = means,
                standard_deviations = standard_deviations,
                correlations = cor,
                fees = fees1),
            Portfolio.Portfolio(
                weights = weights2,
                means = means,
                standard_deviations = standard_deviations,
                correlations = cor,
                fees = fees2),
            Portfolio.Portfolio(
                weights = weights3,
                means = means,
                standard_deviations = standard_deviations,
                correlations = cor,
                fees = fees3),
        ]
        return portfolios