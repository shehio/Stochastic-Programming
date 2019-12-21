# Stochastic-Programming
Problem definition: Given n portfolios, how do you devise an optimal strategy for investment?

This is a program that figures out a long term optimal strategy by choosing between portfolios in each year.
The constratint is that one is only allowed to choose between the previous, current, next portfolios.
We solve this using stochastic programming which is dynamic programming + monte carlo simulation for missing data.

If you come from the computer science society, then this is a simple case of Reinforcement Learning which can be easily solved using value iteration (which we do).
