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
        gamma = 1 / 5000
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

    @staticmethod
    def round_down(money, money_lower_bound, money_upper_bound, step):
        if money <= money_lower_bound:
            return money_lower_bound
        if money >= money_upper_bound:
            return money_upper_bound
        return int(math.ceil(money / float(step))) * step - step

    @staticmethod
    def check_money(money, money_lower_bound, money_upper_bound):
        if money < money_lower_bound:
            raise Exception(f"The value of money shouldn't be less than the lower bound: {money}")
        if money > money_upper_bound:
            raise Exception(f"The value of money shouldn't be greater than the upper bound: {money}")