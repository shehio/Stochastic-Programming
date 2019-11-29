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
        Solution.populateContributions()
        Solution.financial_components = FinancialComponents.FinancialComponents()
        Solution.createValueFunction()
        Solution.PopulateValueFunction()
        Solution.populatePolicy()
        return

    @staticmethod
    def populateContributions():
        for age in range(StartAge, RetirementAge):
            Solution.contributions[age] = round(0.15 * (103.63 - 0.03 * (55 - age)), 2)


    @staticmethod
    def createValueFunction():
        for age in range(StartAge, RetirementAge):
            Solution.valueFunction[age] = {}
            for money in range(MoneyLowerBound, MoneyUpperBound):
                Solution.valueFunction[age][money] = {}
                for portfolio in range(1, Portfolios):
                    Solution.valueFunction[age][money][portfolio] = 0
        # For Retirement Age, the portfolio won't matter anymore
        Solution.valueFunction[RetirementAge] = {}
        for money in range(MoneyLowerBound, MoneyUpperBound):
            Solution.valueFunction[RetirementAge][money] = 0
        return

    @staticmethod
    def PopulateValueFunction():
        # Set the base condition
        targetMoney = 101
        for actualMoney in range(MoneyLowerBound, MoneyUpperBound):
            Solution.valueFunction[RetirementAge][actualMoney] = Solution.financial_components.get_shortfall_utility(actualMoney, targetMoney)

        for age in range(StartAge, RetirementAge): # each stage
            for money in range(MoneyLowerBound, MoneyUpperBound):
                for portfolio in range(1, Portfolios + 1):
                    Solution.getOrComputeValueFunctionAndSetPolicy(age, money, portfolio)
        return

    @staticmethod
    def roundValues(number1, number2, number3, rounding):
        return round(number1, rounding), round(number2, rounding), round(number3, rounding)

    @staticmethod
    def simulateValueFunction(age, money, portfolio):

        val_prev_portfolio = 0
        val_same_portfolio = 0
        val_next_portfolio = 0

        for i in range(SimulationNumber):
            print(portfolio)
            print(Solution.portfolios)
            portfolio_return = Solution.portfolios[portfolio - 1].sample_return()
            total_money = round(money * (1 + portfolio_return) + Solution.contributions[age], 1)

            val_same_portfolio += Solution.getOrComputeValueFunctionAndSetPolicy(age + 1, total_money, portfolio) / SimulationNumber

            if portfolio == 1:
                val_next_portfolio += Solution.getOrComputeValueFunctionAndSetPolicy(age + 1, total_money, portfolio + 1) / SimulationNumber
            elif portfolio == Portfolios:
                val_prev_portfolio += Solution.getOrComputeValueFunctionAndSetPolicy(age + 1, total_money, portfolio - 1) / SimulationNumber
            else:
                val_prev_portfolio += Solution.getOrComputeValueFunctionAndSetPolicy(age + 1, total_money, portfolio - 1) / SimulationNumber
                val_next_portfolio += Solution.getOrComputeValueFunctionAndSetPolicy(age + 1, total_money, portfolio + 1) / SimulationNumber

            return Solution.roundValues(val_prev_portfolio, val_same_portfolio, val_next_portfolio, 2)  # add this to a utility function

    @staticmethod
    def getValueFunction(age, money, portfolio):
        targetMoney = 101
        if not money in Solution.valueFunction[age].keys():
            Solution.valueFunction[age][money] = {}
        if age == RetirementAge:
            Solution.valueFunction[age][money][portfolio] = Solution.financial_components.get_shortfall_utility(money, targetMoney)
        else:
            Solution.valueFunction[age][money][portfolio] = 0
        print("age: " + str(age) + ", money: " + str(money) + ", portfolio: " + str(portfolio))
        print(Solution.valueFunction[age][money][portfolio])
        return Solution.valueFunction[age][money][portfolio]

    @staticmethod
    def setPolicy(age, money, portfolio, value):
        if not age in Solution.policy.keys():
            Solution.policy[age] = {}
        if not money in Solution.policy[age].keys():
            Solution.policy[age][money] = {}

        Solution.policy[age][money][portfolio] = value
        return

    @staticmethod
    def getOrComputeValueFunctionAndSetPolicy(age, money, portfolio):
        if Solution.getValueFunction(age, money, portfolio) == 0:
            val_prev_portfolio, val_same_portfolio, val_next_portfolio = Solution.simulateValueFunction(age, money, portfolio)

            Solution.valueFunction[age][money][portfolio] = np.max([val_prev_portfolio, val_same_portfolio,
                                                                   val_next_portfolio])
            print("portfolio: " + str(portfolio))
            print("np.argmax: " + str(np.argmax([val_prev_portfolio, val_same_portfolio, val_next_portfolio])))
            Solution.setPolicy(age, money, portfolio, portfolio + np.argmax([val_prev_portfolio, val_same_portfolio, val_next_portfolio]) - 1)

        return Solution.valueFunction[age][money][portfolio]

    @staticmethod
    def populatePolicy():
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