import Portfolio
import numpy as np


class PortfolioFactory:

    def __init__(self):
        PortfolioFactory.means = [0.06, 0.059, 0.07, 0.056, 0.019, 0.052, 0.015]
        PortfolioFactory.standard_deviations = [0.091, 0.202, 0.268, 0.207, 0.038, 0.07, 0.058]
        PortfolioFactory.cor = np.array([[1.000, 0.740, 0.670, 0.740, 0.130, 0.470, 0.020],
                                         [0.740, 1.000, 0.700, 0.780, 0.090, 0.460, 0.000],
                                         [0.670, 0.700, 1.000, 0.660, 0.070, 0.450, -0.03],
                                         [0.740, 0.780, 0.660, 1.000, 0.100, 0.370, -0.03],
                                         [0.130, 0.090, 0.070, 0.100, 1.000, 0.100, 0.100],
                                         [0.470, 0.460, 0.450, 0.370, 0.100, 1.000, 0.550],
                                         [0.020, 0.000, -0.03, -0.03, 0.100, 0.550, 1.000]])

    @staticmethod
    def get_available_portfolios():
        weights1 = [0.3, 0.3, 0.1, 0.1, 0.1, 0.1, 0]
        fees1 = 0.2

        weights2 = [0.25, 0.25, 0.1, 0.1, 0.2, 0.1, 0]
        fees2 = 0.18

        weights3 = [0.25, 0.21, 0.08, 0.08, 0.3, 0.08, 0]
        fees3 = 0.16

        weights4 = [0.23, 0.19, 0.06, 0.06, 0.4, 0.06, 0]
        fees4 = 0.14

        weights5 = [0.21, 0.15, 0.04, 0.05, 0.45, 0.05, 0.05]
        fees5 = 0.12

        weights6 = [0.16, 0.12, 0.04, 0.04, 0.5, 0.04, 0.1]
        fees6 = 0.1

        weights7 = [0.13, 0.09, 0.02, 0.03, 0.55, 0.03, 0.15]
        fees7 = 0.08

        weights8 = [0.08, 0.06, 0.01, 0.02, 0.51, 0.02, 0.3]
        fees8 = 0.06

        # Move this into a loop.
        portfolios = [
            PortfolioFactory.create_portfolio(weights1, fees1),
            PortfolioFactory.create_portfolio(weights2, fees2),
            PortfolioFactory.create_portfolio(weights3, fees3),
            PortfolioFactory.create_portfolio(weights4, fees4),
            PortfolioFactory.create_portfolio(weights5, fees5),
            PortfolioFactory.create_portfolio(weights6, fees6),
            PortfolioFactory.create_portfolio(weights7, fees7),
            PortfolioFactory.create_portfolio(weights8, fees8),
        ]

        return portfolios

    @staticmethod
    def create_portfolio(weights, fees):
        return Portfolio.Portfolio(
                weights=weights,
                means=PortfolioFactory.means,
                standard_deviations=PortfolioFactory.standard_deviations,
                correlations=PortfolioFactory.cor,
                fees=fees)


    def test_single_sample(self):
        portfolios = PortfolioFactory.get_available_portfolios()
        count = len(portfolios)
        for i in range(count):
            print(f"Sampling from portfolio: {i + 1}, sample: {portfolios[i].sample_return()}")
            i = i + 1

    def test_portfolio_sampling(self):
        portfolios = PortfolioFactory.get_available_portfolios()
        count = len(portfolios)
        samples = []
        for j in range(count):
            samples.append(0)
        i = 0
        for j in range(10000):
            for portfolio in portfolios:
                samples[i % count] = samples[i % count] + portfolio.sample_return()
                i = i + 1

        for sample in samples:
            print(f"Sampling from portfolio: {i % count}, sample: {sample}")
            i = i + 1


# pf = PortfolioFactory()
# pf.test_single_sample()
# pf.test_portfolio_sampling()
