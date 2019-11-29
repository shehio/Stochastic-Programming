import numpy as np
import FinancialComponents
import PortfolioFactory

MoneyLowerBound = 100
MoneyUpperBound = 103
SimulationNumber = 1000
RetirementAge = 67
StartAge = 65
Portfolios = 3

class ValueFunction:

    def __init__(self):
        self.value_function = {}
        factory = PortfolioFactory.PortfolioFactory()
        self.portfolios = factory.get_available_portfolios()
        self.financial_components = FinancialComponents.FinancialComponents()
        return

    # Sorry for the optional argument but python doesn't allow overloads obviously.
    def get_value_function(self, age, money, portfolio):
        target_money = 101 # remove from here
        if age == RetirementAge:
            if age not in self.value_function.keys() or money not in self.value_function[age].keys():
                self.set_value_function(age, money, self.financial_components.get_shortfall_utility(money, target_money), None)
            return self.value_function[age][money]
        elif age not in self.value_function.keys() or money not in self.value_function[age].keys() or portfolio not in self.value_function[age][money]:
            self.set_value_function(age, money, 0, portfolio)
        return self.value_function[age][money][portfolio]

    # Sorry for the arguments swap, Python doesn't allow overloads.
    def set_value_function(self, age, money, value, portfolio = None):
        if age not in self.value_function.keys():
            self.value_function[age] = {}
        if (portfolio is None):
            self.value_function[age][money] = value
        else:
            if money not in self.value_function[age].keys():
                self.value_function[age][money] = {}
            self.value_function[age][money][portfolio] = value
        return

    def print_value_function(self):
        print(self.value_function)