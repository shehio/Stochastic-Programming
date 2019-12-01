import numpy as np
import sys
import math
import FinancialComponents
import PortfolioFactory

RetirementAge = 67
TargetMoney = 2079 # remove from here
MaxBound = 1000000
MinBound = -1000000

class ValueFunction:

    def __init__(self, money_lower_bound, money_upper_bound, step):
        self.money_lower_bound = money_lower_bound
        self.money_upper_bound = money_upper_bound
        self.value_function = {}
        factory = PortfolioFactory.PortfolioFactory()
        self.portfolios = factory.get_available_portfolios()
        self.financial_components = FinancialComponents.FinancialComponents()
        self.step = step
        self.sets = 0
        return

    # Sorry for the optional argument but python doesn't allow overloads obviously.
    def get_value_function(self, age, money, portfolio): # should be named get or set.
        if age == RetirementAge:
            if age not in self.value_function.keys() or money not in self.value_function[age].keys():
                self.set_value_function(age, money, self.financial_components.get_shortfall_utility(money, TargetMoney), None)
            return self.value_function[age][money]
        elif age not in self.value_function.keys() or money not in self.value_function[age].keys() or portfolio not in self.value_function[age][money]:
            self.set_value_function(age, money, 0, portfolio)
        return self.value_function[age][money][portfolio]

    # Sorry for the arguments swap, Python doesn't allow overloads.
    def set_value_function(self, age, money, value, portfolio = None):
        self.sets = self.sets + 1
        if (self.sets % 1000 == 0):
            print(f"Reached a {self.sets} sets.")

        if age not in self.value_function.keys():
            self.value_function[age] = {}
        if (portfolio is None):
            self.value_function[age][money] = value

        else:
            if money not in self.value_function[age].keys():
                self.value_function[age][money] = {}
            self.value_function[age][money][portfolio] = value
        return

    def print_value_function(self, portfolio_start, age_start, money_start, portfolios, ages, monies):
        value_function_matrix = np.zeros((ages, monies, portfolios), dtype=np.int32) - 1
        annotated_value_function_matrix = np.zeros((ages, monies + 1, portfolios + 1), dtype=np.int32) - 1

        # Trick so that we're able to concatenate these arrays later.
        monies_column = np.zeros((1, monies), dtype=np.int32)
        monies_column[0] = np.array(range(money_start, money_start + monies), dtype=np.int32)

        portfolio_column = np.zeros((1, portfolios + 1), dtype=np.int32)
        portfolio_column[0] = np.array(range(portfolio_start - 1, portfolio_start + portfolios), dtype=np.int32)

        for age in self.value_function.keys():
            for money in self.value_function[age].keys():
                if money >= self.money_upper_bound or money <= self.money_lower_bound:
                    continue
                if age == RetirementAge:
                    for portfolio in range(portfolio_start, portfolio_start + portfolios):
                        value_function_matrix[age - age_start][money - money_start][portfolio - portfolio_start]\
                            = self.value_function[age][money]
                else:
                    for portfolio in self.value_function[age][money].keys():
                        value_function_matrix[age - age_start][money - money_start][portfolio - portfolio_start]\
                            = self.value_function[age][money][portfolio]

        # So that the decision matrix is descriptive
        for age in self.value_function.keys():
            helper = np.concatenate((monies_column.T, value_function_matrix[age - age_start]), axis=1)
            annotated_value_function_matrix[age - age_start] = np.concatenate((portfolio_column, helper), axis=0)

        # To be able to print the whole 3D array
        np.set_printoptions(threshold=sys.maxsize)
        print(annotated_value_function_matrix)