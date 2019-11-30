import numpy as np
import math
import FinancialComponents
import PortfolioFactory

RetirementAge = 67
TargetMoney = 2079 # remove from here


class ValueFunction:

    def __init__(self):
        self.value_function = {}
        factory = PortfolioFactory.PortfolioFactory()
        self.portfolios = factory.get_available_portfolios()
        self.financial_components = FinancialComponents.FinancialComponents()
        return

    # Sorry for the optional argument but python doesn't allow overloads obviously.
    def get_value_function(self, age, money, portfolio):
        money = ValueFunction.money_modification(money)
        if age == RetirementAge:
            if age not in self.value_function.keys() or money not in self.value_function[age].keys():
                self.set_value_function(age, money, self.financial_components.get_shortfall_utility(money, TargetMoney), None)
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

    @staticmethod
    def money_modification(money):
        return math.floor(money)

    @staticmethod
    def roundup(x):
        return int(math.ceil(x / 10.0)) * 10

    def print_value_function(self):
        for age in self.value_function.keys():
            print(f"For age {age}:===========================================================")
            for money in self.value_function[age].keys():
                print(f"For money {money}:")
                print(f"utility becomes: {self.value_function[age][money]}")