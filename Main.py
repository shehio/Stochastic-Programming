import PortfolioFactory as pf
import ValueFunctionCalculator as vfc
import Client as cl
import time
import FinancialComponents
import numpy as np

RetirementAge = 67


class Solution:

    def __init__(self, start_age, initial_balance, step, simulation_number, money_lower_bound, money_upper_bound):
        self.step = step
        self.money_lower_bound = money_lower_bound
        self.money_upper_bound = money_upper_bound
        youngest_client = cl.Client('youngest', start_age, RetirementAge, initial_balance)
        self.portfolios = pf.PortfolioFactory().get_available_portfolios()
        self.value_function_calculator = vfc.ValueFunctionCalculator(
            self.money_lower_bound,
            self.money_upper_bound,
            self.portfolios,
            youngest_client,
            step,
            simulation_number)
        self.value_function_calculator.populate_value_function()
        self.value_function = self.value_function_calculator.value_function.value_function  # Because no encapsulation whatsoever.
        self.policy = self.value_function_calculator.policy.policy  # Because no encapsulation whatsoever.
        Solution.financial_components = FinancialComponents.FinancialComponents()
        return

    # This method is so big and ugly, break it down!
    def calculate_expected_wealth(self, client, simulation_number):
        self.client = client  # Bad practice, should be static.
        wealth_evolution = np.zeros((simulation_number, RetirementAge - self.client.start_age))
        wealth = 0

        for i in range(simulation_number):
            age = self.client.start_age
            money = Solution.financial_components.round_down(
                self.client.get_contribution(age),
                self.money_lower_bound,
                self.money_upper_bound,
                self.step)

            # Amongst all 8.
            value_function_values = list(self.value_function[age][money].values())
            chosen_portfolio = self.portfolios[np.argmax(value_function_values)]
            chosen_portfolio_index = np.argmax(value_function_values) + 1
            m = (1 + chosen_portfolio.sample_return()) * money + self.client.get_contribution(age + 1) # Find a better name
            money = Solution.financial_components.round_down(
                m,
                self.money_lower_bound,
                self.money_upper_bound,
                self.step)
            wealth_evolution[i][age - self.client.start_age] = money
            age = age + 1

            while age is not RetirementAge:
                # print(f"Money: {money}, age: {age}, chosen portfolio: {chosen_portfolio_index}")
                chosen_portfolio_index = self.policy[age][money][chosen_portfolio_index]
                chosen_portfolio = self.portfolios[chosen_portfolio_index - 1]
                money = Solution.financial_components.round_down(
                    (1 + chosen_portfolio.sample_return()) * money + self.client.get_contribution(age + 1),
                    self.money_lower_bound,
                    self.money_upper_bound,
                    self.step)
                wealth_evolution[i][age - self.client.start_age] = money
                age = age + 1

            wealth += money

        expected_wealth = wealth / simulation_number
        expected_wealth_evolution = np.mean(wealth_evolution, axis=0)
        expected_portfolio_choice = self.get_expected_portfolios(expected_wealth_evolution)

        return expected_wealth, expected_wealth_evolution, expected_portfolio_choice

    def get_expected_portfolios(self, expected_wealth_evolution):
        # This vector has one extra item, which is the portfolio we'll choose for the start_year
        expected_portfolio_choice = np.zeros(expected_wealth_evolution.shape[0] + 1, dtype=np.int32)

        # Before making any investments.
        money = Solution.financial_components.round_down(
            self.client.get_contribution(self.client.start_age),
            self.money_lower_bound,
            self.money_upper_bound,
            self.step)

        value_function_values = list(self.value_function[self.client.start_age][money].values())
        expected_portfolio_choice[0] = np.argmax(value_function_values) + 1

        age = self.client.start_age + 1
        for i in range(1, expected_wealth_evolution.shape[0]):
            money = Solution.financial_components.round_down(
                expected_wealth_evolution[i],
                self.money_lower_bound,
                self.money_upper_bound,
                self.step)
            prev_portfolio = expected_portfolio_choice[i - 1]
            # print(f"Money: {money}, age: {age}, prev portfolio: { prev_portfolio}")
            table_portfolio = self.policy[age][money][prev_portfolio]
            # print( f"Money: {money}, age: {age}, chosen portfolio: {prev_portfolio}, table portfolio: {table_portfolio}")
            expected_portfolio_choice[i] = table_portfolio
            age = age + 1

        return expected_portfolio_choice


print(f"Starting the program...")
start = time.time()
solution = Solution(
    start_age=60,
    initial_balance=1000,
    step=10,
    simulation_number=10,
    money_lower_bound=0,
    money_upper_bound=3000)
end = time.time()
print(f"Total execution time in minutes: {(end - start) / 60}")

# Amy = cl.Client('Amy', 50, 67, 1000)
# Bob = cl.Client('Bob', 54, 67, 900)
# Carla = cl.Client('Carla', 54, 67, 500)
# Darrin = cl.Client('Darrin', 57, 67, 1500)
# Eric = cl.Client('Eric', 62, 67, 1200)
Francine = cl.Client('Francine', 65, 67, 1600)


# clients = [Amy, Bob, Carla, Darrin, Eric, Francine]
clients = [Francine]

for simulation_number in np.array([100, 1000, 10000]):
    for client in clients:
        print(f"For client: {client.name}: ")
        expected_wealth, expected_wealth_evolution, expected_portfolio_choice\
            = solution.calculate_expected_wealth(client, simulation_number)
        print(f"Expected wealth: {expected_wealth}")
        print(f"Expected wealth evolution: {expected_wealth_evolution}")
        print(f"Expected portfolio choice: {expected_portfolio_choice}")
