class FinancialComponents:

    @staticmethod
    def get_shortfall_utility(actualMoney, targetMoney):
        exponent = 0.7
        gamma = 1 / 5  # in case of thousands, it should be 1 / 5000
        utility = 0
        if actualMoney > targetMoney:
            utility = (actualMoney ** exponent) / exponent
        else:
            utility = ((actualMoney ** exponent) / exponent) - gamma * (targetMoney - actualMoney)
        return round(utility, 2)