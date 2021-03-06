import Portfolio
import numpy as np


class PortfolioFactory:

    # The means, standard deviations, and correlation matrix are all in log terms.
    def __init__(self):
        PortfolioFactory.log_normal_means = np.array([0.06, 0.059, 0.07, 0.056, 0.019, 0.052, 0.015])
        PortfolioFactory.log_normal_standard_deviations = np.array([[0.19, 0.202, 0.268, 0.207, 0.038, 0.07, 0.058]])
        PortfolioFactory.correlation_matrix = np.array([[1.000, 0.740, 0.670, 0.740, 0.130, 0.470, 0.020],
                                                        [0.740, 1.000, 0.700, 0.780, 0.090, 0.460, 0.000],
                                                        [0.670, 0.700, 1.000, 0.660, 0.070, 0.450, -0.03],
                                                        [0.740, 0.780, 0.660, 1.000, 0.100, 0.370, -0.03],
                                                        [0.130, 0.090, 0.070, 0.100, 1.000, 0.100, 0.100],
                                                        [0.470, 0.460, 0.450, 0.370, 0.100, 1.000, 0.550],
                                                        [0.020, 0.000, -0.03, -0.03, 0.100, 0.550, 1.000]])

        # Transforming log correlation matrix to log covariance matrix.
        standard_deviations_matrix = np.matmul(
            PortfolioFactory.log_normal_standard_deviations.T,
            PortfolioFactory.log_normal_standard_deviations)

        PortfolioFactory.log_normal_covariance_matrix = np.multiply(
            PortfolioFactory.correlation_matrix,
            standard_deviations_matrix)

        # PortfolioFactory.log_normal_covariance_matrix = [round(element, 3) for element in PortfolioFactory.log_normal_covariance_matrix]
        # std_diag = np.diag(PortfolioFactory.log_normal_standard_deviations)
        # PortfolioFactory.log_normal_covariance_matrix = np.dot(std_diag, PortfolioFactory.correlation_matrix, std_diag)

        PortfolioFactory.transform_lognormal_covariance_to_normal()

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
                means=PortfolioFactory.normal_means,
                covariance_matrix=PortfolioFactory.normal_covariance_matrix,
                fees=fees)

    @staticmethod
    def transform_lognormal_covariance_to_normal():
        rows = PortfolioFactory.log_normal_covariance_matrix.shape[0]
        cols = PortfolioFactory.log_normal_covariance_matrix.shape[1]

        PortfolioFactory.normal_covariance_matrix = np.zeros((rows, cols))
        ones = np.ones((1, rows))
        log_means = PortfolioFactory.log_normal_means
        log_std = PortfolioFactory.log_normal_standard_deviations

        normal_means = np.log(ones + log_means) - np.multiply(log_std, log_std) / (2 * ones)
        PortfolioFactory.normal_means = [round(element, 3) for element in normal_means[0]]

        for i in range(0, rows):
            for j in range(0, cols):
                PortfolioFactory.normal_covariance_matrix[i][j] =\
                    round(PortfolioFactory.transform_lognormal_covariance_entry_to_normal(i, j), 5)  # Is 5 okay?

    @staticmethod
    def transform_lognormal_covariance_entry_to_normal(row, col):
        mat = PortfolioFactory.log_normal_covariance_matrix
        log_means = PortfolioFactory.log_normal_means
        return (np.log(1 + ((mat[row][col]) / ((1 + log_means[row]) * (1 + log_means[col])))))

    @staticmethod
    def test_lognormal_to_normal_transformations():
        PortfolioFactory.transform_lognormal_covariance_to_normal()
        print(f"Log Normal Covariance Matrix:")
        print(PortfolioFactory.log_normal_covariance_matrix)
        print(f"Log Normal Means:")
        print(PortfolioFactory.log_normal_means)
        print(f"Normal Covariance Matrix:")
        print(PortfolioFactory.normal_covariance_matrix)
        print(f"Normal Means:")
        print(PortfolioFactory.normal_means)

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
        simulation_number = 15000
        for j in range(simulation_number):
            for portfolio in portfolios:
                samples[i % count] = samples[i % count] + portfolio.sample_return()
                i = i + 1
        print(f"For {simulation_number} number of samples:")
        for sample in samples:
            print(f"Sampling from portfolio: {i % count}, returns: {sample / simulation_number}")
            i = i + 1


# Test code because I'm too lazy to create a test structure for the project.
# pf = PortfolioFactory()
# pf.test_lognormal_to_normal_transformations()
# pf.test_single_sample()
# print()
# pf.test_portfolio_sampling()

