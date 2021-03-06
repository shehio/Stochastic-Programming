import numpy as np
import math
import sys


class Policy:

    def __init__(self):
        self.policy = {}
        return

    @staticmethod
    def money_modification(money):
        return math.floor(money)

    def set_policy(self, age, money, portfolio, value):
        money = Policy.money_modification(money)
        if age not in self.policy.keys():
            self.policy[age] = {}
        if money not in self.policy[age].keys():
            self.policy[age][money] = {}

        self.policy[age][money][portfolio] = value
        return

    def get_policy(self, age, money, portfolio):
        return self.policy[age][money][portfolio]

    def print_policy(self, portfolio_start, age_start, money_start, portfolios, ages, monies, money_lower_bound, money_upper_bound):
        decision_matrix = np.zeros((ages, monies, portfolios), dtype=np.int32) - 1
        annotated_decision_matrix = np.zeros((ages, monies + 1, portfolios + 1), dtype=np.int32) - 1

        # Trick so that we're able to concatenate these arrays later.
        monies_column = np.zeros((1, monies), dtype=np.int32)
        monies_column[0] = np.array(range(money_start, money_start + monies), dtype=np.int32)

        portfolio_column = np.zeros((1, portfolios + 1), dtype=np.int32)
        portfolio_column[0] = np.array(range(portfolio_start - 1, portfolio_start + portfolios), dtype=np.int32)

        for age in self.policy.keys():
            for money in self.policy[age].keys():
                if money >= money_upper_bound or money <= money_lower_bound:
                    continue
                for portfolio in self.policy[age][money].keys():
                    decision_matrix[age - age_start][money - money_start][portfolio - portfolio_start]\
                        = self.policy[age][money][portfolio]

        # So that the decision matrix is descriptive
        for age in self.policy.keys():
            helper = np.concatenate((monies_column.T, decision_matrix[age - age_start]), axis=1)
            annotated_decision_matrix[age - age_start] = np.concatenate((portfolio_column, helper), axis=0)

        # To be able to print the whole 3D array
        np.set_printoptions(threshold=sys.maxsize)
        print(annotated_decision_matrix)
