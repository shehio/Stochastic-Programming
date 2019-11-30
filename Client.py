class Client:

    contributions = {}

    def __init__(self, start_age, retirement_age, initial_balance):
        self.start_age = start_age
        self.retirement_age = retirement_age
        self.initial_balance = initial_balance
        self.populate_contributions()

    def populate_contributions(self):
        for age in range(self.start_age, self.retirement_age):
            self.contributions[age] = round(0.15 * (103.63 - 0.03 * (55 - age)), 2)
            self.contributions[self.start_age] += self.initial_balance
        return

    def get_contribution(self, age):
        return self.contributions[age]
