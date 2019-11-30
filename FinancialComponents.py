import math

EPS = 0.0001


class FinancialComponents:

    # This method can not return 0. In the precision we're using, the values 1111 and 2079 would return a -0.0
    # which would mess up the state of the program. To prevent this we add an epsilon in case we have a zero so that
    # it doesn't intervene with the logic from the rest of the program. We well know that this solution is not optimal,
    # but we choose our battles carefully, and we limit the time we want to allocate for a proper fix.
    @staticmethod
    def get_shortfall_utility(actual_money, target_money):

        exponent = 0.7
        gamma = 1 / 5  # in case of thousands, it should be 1 / 5000
        utility = 0
        if actual_money > target_money:
            utility = (actual_money ** exponent) / exponent
        else:
            utility = ((actual_money ** exponent) / exponent) - gamma * (target_money - actual_money)

        decimal = utility - math.floor(utility)
        utility = math.floor(utility)
        if utility == 0.0:
            utility += EPS

        utility = utility + decimal

        return utility
