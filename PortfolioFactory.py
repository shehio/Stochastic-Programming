import Portfolio


class PortfolioFactory:

    @staticmethod
    def get_available_portfolios():
        portfolios = [Portfolio.Portfolio([0.5, 0.5], [0.10, 0.20], [0.20, 0.40], [[1, 0.3], [0.3, 1]], 0.2),
                      Portfolio.Portfolio([0.7, 0.3], [0.10, 0.20], [0.20, 0.40], [[1, 0.3], [0.3, 1]], 0.2),
                      Portfolio.Portfolio([0, 1], [0.10, 0.20], [0.20, 0.40], [[1, 0.3], [0.3, 1]], 0.2)]
        return portfolios