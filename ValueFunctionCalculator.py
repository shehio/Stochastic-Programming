import numpy as np
import time
import math
import ValueFunction
import FinancialComponents
import Policy
import ClientHelper

RetirementAge = 67


class ValueFunctionCalculator:

    def __init__(self, money_lower_bound, money_upper_bound, portfolios, step, simulation_number):
        # You could probably add a couple of asserts to make sure the input is valid.
        self.step = step
        self.simulation_number = simulation_number
        self.money_lower_bound = money_lower_bound
        self.money_upper_bound = money_upper_bound
        self.portfolios = portfolios
        self.value_function = ValueFunction.ValueFunction(self.money_lower_bound, self.money_upper_bound, self.step)
        self.financial_components = FinancialComponents.FinancialComponents()
        self.policy = Policy.Policy()
        return

    def populate_value_function(self, client):  # The name is incorrect. It does more than it claims.
        client_helper_list = list()

        start = time.time()
        initial_money = client.initial_balance + client.get_contribution(client.start_age)
        age = client.start_age
        for portfolio in range(1, len(self.portfolios) + 1):
            client_helper_list.append(self.get_or_compute_value_function(age, initial_money, portfolio, client))
        end = time.time()
        print(f"For age: {age}, the execution time was {(end - start) / 60} minutes")

        return client_helper_list

    def get_or_compute_value_function(self, age, money, portfolio, client):
        money = self.financial_components.round_down(money, self.money_lower_bound, self.money_upper_bound, self.step)  # Huge optimization
        value = self.value_function.get_value_function(age, money, portfolio)

        if value == 0:
            client_helper = self.simulate_value_function(
                age,
                money,
                portfolio,
                client.get_contribution(age),
                client)
        else:
            if age == RetirementAge:
                client_helper = ClientHelper.ClientHelper(age, money, portfolio, value, None)
            else:
                # Fetch client helper from a map or something
                client_helper = self.value_function.get_client_helper(age, money, portfolio)
        return client_helper

    def simulate_value_function(self, age, money, portfolio, contribution, client):
        val_prev_portfolio = 0
        val_same_portfolio = 0
        val_next_portfolio = 0
        monies = 0

        val_prev_portfolio_ref = None
        val_same_portfolio_ref = None
        val_next_portfolio_ref = None
        returns = 0
        money_diff = 0
        for i in range(self.simulation_number):
            portfolio_return = self.portfolios[portfolio - 1].sample_return()  # portfolios are one-based, hence the - 1
            total_money = np.floor(money * (1 + portfolio_return) + contribution)
            monies += total_money
            money_diff += total_money - money
            returns += portfolio_return

            val_same_portfolio_ref = self.get_or_compute_value_function(age + 1, total_money, portfolio, client)
            val_same_portfolio += val_same_portfolio_ref.value

            if portfolio == 1:
                val_prev_portfolio = -math.inf
                val_next_portfolio_ref = self.get_or_compute_value_function(age + 1, total_money, portfolio + 1, client)
                val_next_portfolio += val_next_portfolio_ref.value
            elif portfolio == len(self.portfolios):
                val_prev_portfolio_ref = self.get_or_compute_value_function(age + 1, total_money, portfolio - 1, client)
                val_prev_portfolio += val_prev_portfolio_ref.value
                val_next_portfolio = -math.inf
            else:
                val_prev_portfolio_ref = self.get_or_compute_value_function(age + 1, total_money, portfolio - 1, client)
                val_prev_portfolio += val_prev_portfolio_ref.value
                val_next_portfolio_ref = self.get_or_compute_value_function(age + 1, total_money, portfolio + 1, client)
                val_next_portfolio += val_next_portfolio_ref.value

        monies_average = monies / self.simulation_number

        val_prev_portfolio, val_same_portfolio, val_next_portfolio = self.round_values(
            val_prev_portfolio / self.simulation_number,
            val_same_portfolio / self.simulation_number,
            val_next_portfolio / self.simulation_number,
            2)

        # Set the value function and policy
        values = [val_prev_portfolio, val_same_portfolio, val_next_portfolio]
        largest_value_index = np.argmax(values)
        max_value = values[largest_value_index]
        self.value_function.set_value_function(age, money, max_value, portfolio)

        chosen_portfolio = portfolio - 1 + largest_value_index
        self.policy.set_policy(age, money, portfolio, chosen_portfolio)

        # Set the client helper.
        max_value_ref = self.get_or_compute_value_function(age + 1, monies_average, chosen_portfolio, client)
        client_helper = ClientHelper.ClientHelper(age, money, chosen_portfolio, max_value, max_value_ref)

        # cache it
        self.value_function.set_client_helper(age, money, client_helper, portfolio)
        return client_helper

    @staticmethod
    def round_values(number1, number2, number3, rounding):
        return round(number1, rounding), round(number2, rounding), round(number3, rounding)
