import PortfolioFactory as pf
import ValueFunctionCalculator as vfc
import Client as cl

# StartAge = 50
# RetirementAge = 67
# Portfolios = 8
# MoneyLowerBound = 1000
# MoneyUpperBound = 2500

# Test parameters
RetirementAge = 67
Portfolios = 3
MoneyLowerBound = 2000
MoneyUpperBound = 2100
SimulationNumber = 1000


class Solution:

    # Move Client data to their own class
    portfolios = []
    value_function = None
    contributions = {}
    policy = {}

    def __init__(self, start_age, initial_balance):
        self.client = cl.Client(start_age, RetirementAge, initial_balance)
        self.portfolios = pf.PortfolioFactory().get_available_portfolios()
        self.value_function_calculator = vfc.ValueFunctionCalculator(
            MoneyLowerBound, MoneyUpperBound, self.portfolios, self.client)
        self.value_function_calculator.populate_value_function()
        # Solution.populate_policy()
        return

    @staticmethod
    def set_policy(age, money, portfolio, value):
        if age not in Solution.policy.keys():
            Solution.policy[age] = {}
        if money not in Solution.policy[age].keys():
            Solution.policy[age][money] = {}

        Solution.policy[age][money][portfolio] = value
        return

    # @staticmethod
    # def populate_policy():
    #     # For Retirement Age, we don't need any actions anymore.
    #     for age in range(StartAge, RetirementAge):
    #         Solution.policy[age] = {}
    #         for money in range(MoneyLowerBound, MoneyUpperBound):
    #             Solution.policy[age][money] = {}
    #             for portfolio in range(1, Portfolios):
    #                 Solution.policy[age][money][portfolio] = 0
    #     return


c1 = Solution(start_age=66, initial_balance=1000)