import numpy as np
import math
import ValueFunction
import FinancialComponents
import Policy

SimulationNumber = 1000
RetirementAge = 67


class ValueFunctionCalculator:

    def __init__(self, money_lower_bound, money_upper_bound, portfolios, client):
        self.money_lower_bound = money_lower_bound
        self.money_upper_bound = money_upper_bound
        self.portfolios = portfolios
        self.value_function = ValueFunction.ValueFunction()
        self.financial_components = FinancialComponents.FinancialComponents()
        self.client = client
        self.policy = Policy.Policy()
        return

    def populate_value_function(self):
        # Set the base condition

        for age in range(self.client.start_age, RetirementAge):  # each stage
            print(f"Working on age: {age}")
            for money in range(self.money_lower_bound, self.money_upper_bound):
                for portfolio in range(1, len(self.portfolios) + 1):
                    self.get_or_compute_value_function(age, money, portfolio)
        # self.value_function.print_value_function()
        self.policy.print_policy(
            portfolio_start=1,
            age_start=self.client.start_age,
            money_start=self.money_lower_bound,
            portfolios=len(self.portfolios),
            ages=RetirementAge - self.client.start_age,
            monies=self.money_upper_bound - self.money_lower_bound)
        return

    def get_or_compute_value_function(self, age, money, portfolio):
        value = self.value_function.get_value_function(age, money, portfolio)
        if value == 0:
            val_prev_portfolio, val_same_portfolio, val_next_portfolio = self.simulate_value_function(
                age, money, portfolio, self.client.get_contribution(age))
            self.value_function.set_value_function(
                age, money, np.max([val_prev_portfolio, val_same_portfolio, val_next_portfolio]), portfolio)
            value = self.value_function.get_value_function(age, money, portfolio)
            self.policy.set_policy(age, money, portfolio, portfolio + np.argmax([val_prev_portfolio, val_same_portfolio, val_next_portfolio]) - 1)

        return value

    def simulate_value_function(self, age, money, portfolio, contribution):
        val_prev_portfolio = 0
        val_same_portfolio = 0
        val_next_portfolio = 0

        for i in range(SimulationNumber):
            portfolio_return = self.portfolios[portfolio - 1].sample_return()
            total_money = np.floor(money * (1 + portfolio_return) + contribution)

            val_same_portfolio += self.get_or_compute_value_function(age + 1, total_money, portfolio) / SimulationNumber
            # print(f"The value of the same portfolio is: {val_same_portfolio} in simulation number: {i}")

            if portfolio == 1:
                val_next_portfolio += self.get_or_compute_value_function(age + 1, total_money,
                                                                         portfolio + 1) / SimulationNumber
            elif portfolio == len(self.portfolios):
                val_prev_portfolio += self.get_or_compute_value_function(age + 1, total_money,
                                                                         portfolio - 1) / SimulationNumber
            else:
                val_prev_portfolio += self.get_or_compute_value_function(age + 1, total_money,
                                                                         portfolio - 1) / SimulationNumber
                val_next_portfolio += self.get_or_compute_value_function(age + 1, total_money,
                                                                         portfolio + 1) / SimulationNumber

        return self.round_values(val_prev_portfolio, val_same_portfolio, val_next_portfolio, 2)

    @staticmethod
    def round_values(number1, number2, number3, rounding):
        return math.floor(number1), math.floor(number2), math.floor(number3)
        # return round(number1, rounding), round(number2, rounding), round(number3, rounding)

