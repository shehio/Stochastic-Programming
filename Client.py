class Client:

    def __init__(self, name, start_age, retirement_age, initial_balance):
        self.name = name
        self.start_age = start_age
        self.retirement_age = retirement_age
        self.initial_balance = initial_balance
        self.contributions = {}
        self.populate_contributions()

    def populate_contributions(self):
        for age in range(self.start_age, self.retirement_age):
            self.contributions[age] = round(0.15 * (103.63 - 0.03 * (55 - age)), 2)
        if self.start_age in self.contributions:
            self.contributions[self.start_age] += self.initial_balance
        else:
            self.contributions[self.start_age] = self.initial_balance
        self.contributions[self.retirement_age] = 0
        return

    def get_contribution(self, age):
        return self.contributions[age]
