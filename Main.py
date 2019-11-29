import numpy as np
import PortfolioFactory
import FinancialComponents
import ValueFunction as vf

# StartAge = 50
# RetirementAge = 67
# Portfolios = 8
# MoneyLowerBound = 1000
# MoneyUpperBound = 2500

# Test parameters
StartAge = 65
RetirementAge = 67
Portfolios = 3
MoneyLowerBound = 100
MoneyUpperBound = 103
SimulationNumber = 1000


class Solution:

    # Move Client data to their own class
    # Move policy/value functions somewhere else.
    portfolios = []
    financial_components = None
    valueFunction = {}
    contributions = {}
    policy = {}

    def __init__(self):
        factory = PortfolioFactory.PortfolioFactory()
        Solution.portfolios = factory.get_available_portfolios()
        Solution.populate_contributions()
        Solution.financial_components = FinancialComponents.FinancialComponents()
        Solution.populate_value_function()
        Solution.populate_policy()
        return

    @staticmethod
    def populate_contributions():
        for age in range(StartAge, RetirementAge):
            Solution.contributions[age] = round(0.15 * (103.63 - 0.03 * (55 - age)), 2)

    @staticmethod
    def round_values(number1, number2, number3, rounding):
        return round(number1, rounding), round(number2, rounding), round(number3, rounding)

    @staticmethod
    def set_policy(age, money, portfolio, value):
        if age not in Solution.policy.keys():
            Solution.policy[age] = {}
        if money not in Solution.policy[age].keys():
            Solution.policy[age][money] = {}

        Solution.policy[age][money][portfolio] = value
        return

    @staticmethod
    def populate_policy():
        # For Retirement Age, we don't need any actions anymore.
        for age in range(StartAge, RetirementAge):
            Solution.policy[age] = {}
            for money in range(MoneyLowerBound, MoneyUpperBound):
                Solution.policy[age][money] = {}
                for portfolio in range(1, Portfolios):
                    Solution.policy[age][money][portfolio] = 0
        return


c1 = Solution()
print(Solution.valueFunction)
print(Solution.contributions)
