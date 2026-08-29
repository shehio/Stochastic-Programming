import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import Portfolio
import PortfolioFactory


def test_fees_are_management_fees_not_percentages():
    PortfolioFactory.PortfolioFactory()
    fees = [portfolio.fees for portfolio in PortfolioFactory.PortfolioFactory.get_available_portfolios()]

    # 0.20% down to 0.06% a year, most aggressive portfolio first.
    assert fees == sorted(fees, reverse=True)
    assert all(0 < fee < 0.01 for fee in fees)


def test_fee_comes_off_the_return_level():
    PortfolioFactory.PortfolioFactory()
    fee = 0.002
    weights = [0.3, 0.3, 0.1, 0.1, 0.1, 0.1, 0]

    charged = PortfolioFactory.PortfolioFactory.create_portfolio(weights, fee)
    free = PortfolioFactory.PortfolioFactory.create_portfolio(weights, 0)

    simulations = 20000
    np.random.seed(1)
    net = sum(charged.sample_return() for _ in range(simulations)) / simulations
    np.random.seed(1)
    gross = sum(free.sample_return() for _ in range(simulations)) / simulations

    # A management fee is a fixed haircut on the level, not a share of the return.
    assert abs((gross - net) - fee) < 5e-4


def test_fee_is_charged_in_a_losing_year():
    # A single asset that always loses: zero covariance, so the draw is the mean.
    always_loses = Portfolio.Portfolio(
        weights=[1.0],
        means=[-0.3],
        covariance_matrix=np.zeros((1, 1)),
        fees=0.002)
    free = Portfolio.Portfolio(
        weights=[1.0],
        means=[-0.3],
        covariance_matrix=np.zeros((1, 1)),
        fees=0)

    # Multiplying by (1 - fee) shrinks a negative return towards zero, so the
    # fee used to pay the client in a down year.
    assert always_loses.sample_return() < free.sample_return()


if __name__ == '__main__':
    for name, test in sorted(globals().items()):
        if name.startswith('test_'):
            test()
            print(f"{name}: ok")
