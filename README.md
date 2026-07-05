# Stochastic-Programming
Problem definition: Given n portfolios, how do you devise an optimal strategy for investment?

This is a program that figures out a long term optimal strategy by choosing between portfolios in each year. The constraint is that one is only allowed to choose between the previous, current, next portfolios. We solve this using stochastic programming, which is dynamic programming + Monte Carlo simulation for missing data.

If you come from the computer science society, then this is a simple case of Reinforcement Learning which can be easily solved using value iteration (which we do).

## The model

- A client starts at some age with an initial balance, contributes a salary-based amount every year, and retires at 67 with a target balance.
- There are 8 available portfolios built from 7 asset classes, ordered from aggressive to conservative, each with its own fee. Asset returns are sampled from a multivariate lognormal distribution: arithmetic (simple-return) means, standard deviations, and correlations are moment-matched to the parameters of the underlying multivariate normal.
- **State:** (age, wealth bucket, current portfolio). Wealth is discretized into buckets of size `step` between a lower and an upper bound.
- **Action:** each year, stay in the current portfolio or move to the adjacent one (previous/next).
- **Reward:** at retirement, a shortfall utility — CRRA-style utility of wealth (`w^0.7 / 0.7`), minus a linear penalty when wealth falls short of the target.
- **Solution:** backward-recursive value iteration. The value of each (state, action) pair is estimated by Monte Carlo simulation (`simulation_number` samples of portfolio returns per state), memoized so every state is computed once.

The output for each client is the optimal expected value per starting portfolio, plus a representative trajectory (age, wealth, chosen portfolio, value) to retirement.

## How to run

Requires Python 3.9+ and numpy (see `requirements.txt`).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python Main.py
```

Clients, wealth bounds, bucket `step`, and `simulation_number` are configured at the bottom of `Main.py`. Runtime grows with the number of wealth buckets and simulations; the defaults take a few minutes.

## Code map

| File | Purpose |
|---|---|
| `Main.py` | Entry point: defines clients and solver parameters, prints trajectories. |
| `Client.py` | Client profile: ages, initial balance, yearly contributions. |
| `PortfolioFactory.py` | The 8 portfolios and the lognormal-to-normal parameter transformations. |
| `Portfolio.py` | Samples a fee-adjusted portfolio return from the multivariate lognormal. |
| `ValueFunctionCalculator.py` | The backward-recursive Monte Carlo value iteration. |
| `ValueFunction.py` | Memoized value function keyed by (age, money, portfolio). |
| `Policy.py` | Stores and prints the optimal decision per state. |
| `FinancialComponents.py` | Shortfall utility and wealth-bucket rounding. |
| `ClientHelper.py` | Linked-list node for printing a client's trajectory. |
