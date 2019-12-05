import PortfolioFactory as pf
import ValueFunctionCalculator as vfc
import Client as cl
import time
import math
import numpy as np

RetirementAge = 67
MoneyLowerBound = 0
MoneyUpperBound = 3000
SimulationNumber = 100


class Solution:

    def __init__(self, start_age, initial_balance, step):
        self.step = step
        self.client = cl.Client(start_age, RetirementAge, initial_balance)
        self.portfolios = pf.PortfolioFactory().get_available_portfolios()
        self.value_function_calculator = vfc.ValueFunctionCalculator(
            MoneyLowerBound, MoneyUpperBound, self.portfolios, self.client, step, SimulationNumber)
        self.value_function_calculator.populate_value_function()
        self.value_function = self.value_function_calculator.value_function.value_function  # Because no encapsulation whatsoever.
        self.policy = self.value_function_calculator.policy.policy  # Because no encapsulation whatsoever.
        return

    def calculate_expected_wealth(self, simulation_number):
        wealth = 0
        for i in range(simulation_number):
            age = self.client.start_age
            money = self.round_down(self.client.get_contribution(age))
            # Amongst all 8.
            value_function_values = list(self.value_function[age][money].values())

            chosen_portfolio_index = np.argmax(value_function_values) + 1
            chosen_portfolio = self.portfolios[chosen_portfolio_index - 1]
            money = self.round_down(
                (1 + chosen_portfolio.sample_return()) * money + self.client.get_contribution(age + 1))
            age = age + 1
            # print(F"Initially money: {money} at age: {age}")

            while age is not RetirementAge:
                chosen_portfolio_index = self.policy[age][money][chosen_portfolio_index]
                chosen_portfolio = self.portfolios[chosen_portfolio_index - 1]
                money = self.round_down(
                    (1 + chosen_portfolio.sample_return()) * money + self.client.get_contribution(age + 1))
                age = age + 1
                # print(f"Money: {money}, age: {age}, chosen portfolio: {chosen_portfolio_index}")
            wealth += money
        return wealth / simulation_number

    def round_down(self, money):
        if money <= 0:
            return 0
        return int(math.ceil(money / float(self.step))) * self.step - self.step


print(f"Starting the program...")
start = time.time()
solution = Solution(start_age=65, initial_balance=1600, step=10)
end = time.time()

print(f"Total execution time in minutes: {(end - start) / 60}")
print(f"Expected Wealth: {solution.calculate_expected_wealth(100)}")
print(f"Expected Wealth: {solution.calculate_expected_wealth(1000)}")
print(f"Expected Wealth: {solution.calculate_expected_wealth(10000)}")
print(f"Expected Wealth: {solution.calculate_expected_wealth(100000)}")
