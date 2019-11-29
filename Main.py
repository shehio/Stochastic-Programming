import numpy as np

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

class Portfolio:
    def __init__(self):
        return

class Solution:

    valueFunction = {}
    fees = {}
    contributions = {}
    portfoliosReturns = {}
    portfoliosVariances = {}
    policy = {}

    def __init__(self):
        Solution.PopulatePortfoliosReturnsAndVariance()
        Solution.populateContributions()
        Solution.populateFees()
        Solution.createValueFunction()
        Solution.PopulateValueFunction()
        Solution.populatePolicy()

        return

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
            Solution.valueFunction[RetirementAge][actualMoney] = Solution.computeUtilityFunction(actualMoney, targetMoney)

        for age in range(StartAge, RetirementAge): # each stage
            for money in range(MoneyLowerBound, MoneyUpperBound):
                for portfolio in range(1, Portfolios + 1):
                    Solution.getOrComputeValueFunctionAndSetPolicy(age, money, portfolio)
        return

    @staticmethod
    def SampleReturn(mean, variance):
        return mean

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
            portfolio_return = Solution.SampleReturn(Solution.portfoliosReturns[portfolio], Solution.portfoliosVariances[portfolio])
            total_money = round(money * (1 + portfolio_return - Solution.fees[portfolio]) + Solution.contributions[age], 1)

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
            Solution.valueFunction[age][money][portfolio] = Solution.computeUtilityFunction(money, targetMoney)
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

    @staticmethod
    def PopulatePortfoliosReturnsAndVariance():
        ## Dummy numbers to get on with the rest of the problem for now.
        mu = 0.06  # np.random.lognormal(0, 1)
        sigma = 0.12  # np.random.lognormal(0, 1)
        for portfolio in range(1, Portfolios + 1):
            Solution.portfoliosReturns[portfolio] = mu
            Solution.portfoliosVariances[portfolio] = sigma
        return

    @staticmethod
    def populateContributions():
        for age in range(StartAge, RetirementAge):
            Solution.contributions[age] = round(0.15 * (103.63 - 0.03 * (55 - age)), 2)

    @staticmethod
    def populateFees():
        for portfolio in range(1, 9):
            Solution.fees[portfolio] = round(0.2 - (portfolio - 1) * 0.02, 2)

    @staticmethod
    def computeUtilityFunction(actualMoney, targetMoney):
        exponent = 0.7
        gamma = 1 / 5  # in case of thousands, it should be 1 / 5000
        utility = 0
        if actualMoney > targetMoney:
            utility = (actualMoney ** exponent) / exponent
        else:
            utility = ((actualMoney ** exponent) / exponent) - gamma * (targetMoney - actualMoney)
        return round(utility, 2)


    # def ValueFunction(age, actualMoney, portfolio):
    #     # Backward recursion in place
    #     if age >= RetirementAge:
            # return ValueFunctionTable[actualMoney] # We don't care about age or portfolio.



c1 = Solution()

print(Solution.valueFunction)
print(Solution.portfoliosReturns)
print(Solution.portfoliosVariances)
print(Solution.contributions)
print(Solution.fees)
# table = {1: {}}
# table[1][1] = {}
# table[1][1][1] = 4
# print(table[1])
# print(table[1][1])
# print(table[1][1][1])
# for age in range(50, 67):
#     print(round(SalaryInThousandsForCurrentAge(age), 2))