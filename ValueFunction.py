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

    def populate_value_function(self, money_lower_bound, money_upper_bound):
        # Set the base condition
        target_money = 101
        for actual_money in range(money_lower_bound, money_upper_bound):
            self.set_value_function(RetirementAge, actual_money, self.financial_components.get_shortfall_utility(actual_money, target_money))

        for age in range(StartAge, RetirementAge): # each stage
            for money in range(MoneyLowerBound, MoneyUpperBound):
                for portfolio in range(1, Portfolios + 1):
                    self.get_or_compute_value_function_and_set_policy(age, money, portfolio)
        return

    def get_or_compute_value_function_and_set_policy(self, age, money, portfolio):
        value = self.get_value_function(age, money, portfolio)

        if  value == 0:
            val_prev_portfolio, val_same_portfolio, val_next_portfolio = \
            self.simulate_value_function(age, money,portfolio, 0)

            self.set_value_function(age, money, portfolio, np.max([val_prev_portfolio, val_same_portfolio,
                                                                   val_next_portfolio]))
            value = self.get_value_function(age, money, portfolio)
#             self.set_policy(age, money, portfolio,
#                                 portfolio + np.argmax([val_prev_portfolio, val_same_portfolio, val_next_portfolio]) - 1)

        return value

    def simulate_value_function(self, age, money, portfolio, contribution):

        val_prev_portfolio = 0
        val_same_portfolio = 0
        val_next_portfolio = 0

        for i in range(SimulationNumber):
            portfolio_return = self.portfolios[portfolio - 1].sample_return()
            total_money = round(money * (1 + portfolio_return) + contribution, 1)

            val_same_portfolio += self.get_or_compute_value_function_and_set_policy(age + 1, total_money,
                                                                                        portfolio) / SimulationNumber

            if portfolio == 1:
                val_next_portfolio += self.get_or_compute_value_function_and_set_policy(age + 1, total_money,
                                                                                            portfolio + 1) / SimulationNumber
            elif portfolio == Portfolios:
                val_prev_portfolio += self.get_or_compute_value_function_and_set_policy(age + 1, total_money,
                                                                                            portfolio - 1) / SimulationNumber
            else:
                val_prev_portfolio += self.get_or_compute_value_function_and_set_policy(age + 1, total_money,
                                                                                            portfolio - 1) / SimulationNumber
                val_next_portfolio += self.get_or_compute_value_function_and_set_policy(age + 1, total_money,
                                                                                            portfolio + 1) / SimulationNumber

            return self.round_values(val_prev_portfolio, val_same_portfolio, val_next_portfolio,
                                         2)  # add this to a utility function

    # Sorry for the optional argument but python doesn't allow overloads obviously.
    def get_value_function(self, age, money, portfolio):
#         print(f"age: {age}")
        target_money = 101 # remove from here
        if age == RetirementAge:
            if age not in self.value_function.keys() or money not in self.value_function[age].keys():
                self.set_value_function(age, money, self.financial_components.get_shortfall_utility(money, target_money), None)
            return self.value_function[age][money]
        elif age not in self.value_function.keys() or money not in self.value_function[age].keys() or portfolio not in self.value_function[age][money]:
            self.set_value_function(age, money, 0, portfolio)
        print(f"RETURNED: age: {age}, money: {money}, portfolio: {portfolio}")
        return self.value_function[age][money][portfolio]

    # Sorry for the arguments swap, Python doesn't allow overloads.
    def set_value_function(self, age, money, value, portfolio = None):
        print(f"age: {age}, money: {money}, value: {value}, portfolio: {portfolio}")
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
    def round_values(number1, number2, number3, rounding):
        return round(number1, rounding), round(number2, rounding), round(number3, rounding)


vf = ValueFunction()
vf.populate_value_function(100, 102)