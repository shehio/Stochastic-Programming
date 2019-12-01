import PortfolioFactory as pf
import ValueFunctionCalculator as vfc
import Client as cl
import time

RetirementAge = 67
MoneyLowerBound = 0
MoneyUpperBound = 3000
SimulationNumber = 100


class Solution:

    def __init__(self, start_age, initial_balance, step):
        self.client = cl.Client(start_age, RetirementAge, initial_balance)
        self.portfolios = pf.PortfolioFactory().get_available_portfolios()
        self.value_function_calculator = vfc.ValueFunctionCalculator(
            MoneyLowerBound, MoneyUpperBound, self.portfolios, self.client, step, SimulationNumber)
        self.value_function_calculator.populate_value_function()
        return


print(f"Starting the program...")
start = time.time()
Solution(start_age=65, initial_balance=1600, step=10)
end = time.time()
print(f"Total execution time in minutes: {(end - start) / 60}")

