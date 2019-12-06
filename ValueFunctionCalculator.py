import numpy as np
import time
import math
import ValueFunction
import FinancialComponents
import Policy

RetirementAge = 67


class ValueFunctionCalculator:

    def __init__(self, money_lower_bound, money_upper_bound, portfolios, client, step, simulation_number):
        # You could probably add a couple of asserts to make sure the input is valid.
        self.step = step
        self.simulation_number = simulation_number
        self.money_lower_bound = money_lower_bound
        self.money_upper_bound = money_upper_bound
        self.client = client
        self.portfolios = portfolios
        self.value_function = ValueFunction.ValueFunction(self.money_lower_bound, self.money_upper_bound, self.step)
        self.financial_components = FinancialComponents.FinancialComponents()
        self.policy = Policy.Policy()

        return

    def populate_value_function(self):  # The name is incorrect. It does more it claims.
        for age in range(self.client.start_age, RetirementAge + 1):  # each stage
            start = time.time()
            for money in range(self.money_lower_bound, self.money_upper_bound + 1, self.step):
                for portfolio in range(1, len(self.portfolios) + 1):
                    self.get_or_compute_value_function(age, money, portfolio)
            end = time.time()
            print(f"For age: {age}, the execution time was {(end - start) / 60} minutes")

        self.value_function.print_value_function(
            portfolio_start=1,
            age_start=self.client.start_age,
            money_start=self.money_lower_bound,
            portfolios=len(self.portfolios),
            ages=RetirementAge - self.client.start_age + 1,
            monies=self.money_upper_bound - self.money_lower_bound)
        self.policy.print_policy(
            portfolio_start=1,
            age_start=self.client.start_age,
            money_start=self.money_lower_bound,
            portfolios=len(self.portfolios),
            ages=RetirementAge - self.client.start_age,
            monies=self.money_upper_bound - self.money_lower_bound,
            money_lower_bound=self.money_lower_bound,
            money_upper_bound=self.money_upper_bound)
        return

    def get_or_compute_value_function(self, age, money, portfolio):
        money = self.financial_components.round_down(money, self.money_lower_bound, self.money_upper_bound, self.step)  # Huge optimization
        value = self.value_function.get_value_function(age, money, portfolio)

        if value == 0:
            val_prev_portfolio, val_same_portfolio, val_next_portfolio = self.simulate_value_function(
                age, money, portfolio, self.client.get_contribution(age))
            self.value_function.set_value_function(
                age, money, np.max([val_prev_portfolio, val_same_portfolio, val_next_portfolio]), portfolio)
            value = self.value_function.get_value_function(age, money, portfolio)
            self.policy.set_policy(age, money, portfolio, portfolio - 1 + np.argmax([val_prev_portfolio, val_same_portfolio, val_next_portfolio]))

        return value

    def simulate_value_function(self, age, money, portfolio, contribution):
        val_prev_portfolio = 0
        val_same_portfolio = 0
        val_next_portfolio = 0

        for i in range(self.simulation_number):
            portfolio_return = self.portfolios[portfolio - 1].sample_return()  # portfolios are one-based, hence the - 1
            total_money = np.floor(money * (1 + portfolio_return) + contribution)

            val_same_portfolio += self.get_or_compute_value_function(age + 1, total_money, portfolio)

            if portfolio == 1:
                val_next_portfolio += self.get_or_compute_value_function(age + 1, total_money, portfolio + 1)
                val_prev_portfolio = -math.inf
            elif portfolio == len(self.portfolios):
                val_prev_portfolio += self.get_or_compute_value_function(age + 1, total_money, portfolio - 1)
                val_next_portfolio = -math.inf
            else:
                val_prev_portfolio += self.get_or_compute_value_function(age + 1, total_money, portfolio - 1)
                val_next_portfolio += self.get_or_compute_value_function(age + 1, total_money, portfolio + 1)

        return self.round_values(
            val_prev_portfolio / self.simulation_number,
            val_same_portfolio / self.simulation_number,
            val_next_portfolio / self.simulation_number, 2)

    @staticmethod
    def round_values(number1, number2, number3, rounding):
        return round(number1, rounding), round(number2, rounding), round(number3, rounding)
