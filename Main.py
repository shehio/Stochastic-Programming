import PortfolioFactory as pf
import ValueFunctionCalculator as vfc
import Client as cl
import time

# StartAge = 50
# RetirementAge = 67
# Portfolios = 8
# MoneyLowerBound = 1000
# MoneyUpperBound = 2500

# Test parameters
RetirementAge = 67
Portfolios = 3
MoneyLowerBound = 2400
MoneyUpperBound = 2500
SimulationNumber = 1000


class Solution:

    def __init__(self, start_age, initial_balance):
        self.client = cl.Client(start_age, RetirementAge, initial_balance)
        self.portfolios = pf.PortfolioFactory().get_available_portfolios()
        self.value_function_calculator = vfc.ValueFunctionCalculator(
            MoneyLowerBound, MoneyUpperBound, self.portfolios, self.client)
        self.value_function_calculator.populate_value_function()
        return

start = time.time()
Solution(start_age=66, initial_balance=1000)
end = time.time()
print(end - start)

