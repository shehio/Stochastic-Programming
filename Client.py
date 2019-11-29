class Client:

    contributions = {}

    def __init__(self, start_age, retirement_age):
        self.start_age = start_age
        self.retirement_age = retirement_age
        self.populate_contributions()

    def populate_contributions(self):
        for age in range(self.start_age, self.retirement_age):
            self.contributions[age] = round(0.15 * (103.63 - 0.03 * (55 - age)), 2)
        return

    def get_contribution(self, age):
        return self.contributions[age]