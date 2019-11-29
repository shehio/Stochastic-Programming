import numpy as np
import PortfolioFactory
import FinancialComponents

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
    def populate_value_function():
        # Set the base condition
        target_money = 101
        for actual_money in range(MoneyLowerBound, MoneyUpperBound):
            Solution.set_value_function(RetirementAge, actual_money, Solution.financial_components.get_shortfall_utility(actual_money, target_money))

        for age in range(StartAge, RetirementAge): # each stage
            for money in range(MoneyLowerBound, MoneyUpperBound):
                for portfolio in range(1, Portfolios + 1):
                    Solution.get_or_compute_value_function_and_set_policy(age, money, portfolio)
        return

    @staticmethod
    def round_values(number1, number2, number3, rounding):
        return round(number1, rounding), round(number2, rounding), round(number3, rounding)

    @staticmethod
    def simulate_value_function(age, money, portfolio):

        val_prev_portfolio = 0
        val_same_portfolio = 0
        val_next_portfolio = 0

        for i in range(SimulationNumber):
            portfolio_return = Solution.portfolios[portfolio - 1].sample_return()
            total_money = round(money * (1 + portfolio_return) + Solution.contributions[age], 1)

            val_same_portfolio += Solution.get_or_compute_value_function_and_set_policy(age + 1, total_money,
                                                                                        portfolio) / SimulationNumber

            if portfolio == 1:
                val_next_portfolio += Solution.get_or_compute_value_function_and_set_policy(age + 1, total_money,
                                                                                            portfolio + 1) / SimulationNumber
            elif portfolio == Portfolios:
                val_prev_portfolio += Solution.get_or_compute_value_function_and_set_policy(age + 1, total_money,
                                                                                            portfolio - 1) / SimulationNumber
            else:
                val_prev_portfolio += Solution.get_or_compute_value_function_and_set_policy(age + 1, total_money,
                                                                                            portfolio - 1) / SimulationNumber
                val_next_portfolio += Solution.get_or_compute_value_function_and_set_policy(age + 1, total_money,
                                                                                            portfolio + 1) / SimulationNumber

            return Solution.round_values(val_prev_portfolio, val_same_portfolio, val_next_portfolio,
                                         2)  # add this to a utility function

    @staticmethod
    def get_value_function(age, money, portfolio):
        targetMoney = 101
        if age not in Solution.valueFunction.keys():
            Solution.valueFunction[age] = {}
        if money not in Solution.valueFunction[age].keys():
            Solution.valueFunction[age][money] = {}
        if age == RetirementAge:
            Solution.valueFunction[age][money][portfolio] = Solution.financial_components.get_shortfall_utility(money, targetMoney)
        else:
            Solution.valueFunction[age][money][portfolio] = 0
        return Solution.valueFunction[age][money][portfolio]

    @staticmethod
    def set_policy(age, money, portfolio, value):
        if age not in Solution.policy.keys():
            Solution.policy[age] = {}
        if money not in Solution.policy[age].keys():
            Solution.policy[age][money] = {}

        Solution.policy[age][money][portfolio] = value
        return

    @staticmethod
    def set_value_function(age, money, portfolio, value):
        if age not in Solution.valueFunction.keys():
            Solution.valueFunction[age] = {}
        if money not in Solution.valueFunction[age].keys():
            Solution.valueFunction[age][money] = {}
            Solution.valueFunction[age][money][portfolio] = value
        return

    # The case for retirement.
    @staticmethod
    def set_value_function(age, money, value):
        if age not in Solution.valueFunction.keys():
            Solution.valueFunction[age] = {}
        Solution.valueFunction[age][money] = value
        return

    @staticmethod
    def get_or_compute_value_function_and_set_policy(age, money, portfolio):
        if Solution.get_value_function(age, money, portfolio) == 0:
            val_prev_portfolio, val_same_portfolio, val_next_portfolio = Solution.simulate_value_function(age, money,
                                                                                                          portfolio)

            Solution.valueFunction[age][money][portfolio] = np.max([val_prev_portfolio, val_same_portfolio,
                                                                   val_next_portfolio])
            Solution.set_policy(age, money, portfolio,
                                portfolio + np.argmax([val_prev_portfolio, val_same_portfolio, val_next_portfolio]) - 1)

        return Solution.valueFunction[age][money][portfolio]

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
