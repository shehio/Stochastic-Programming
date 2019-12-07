class ClientHelper:

    def __init__(self, age, money, portfolio, value, next_helper):
        self.age = age
        self.money = money
        self.portfolio = portfolio
        self.value = value
        self.next = next_helper  # A link to the future helper.
        return

    def print(self):
        pointer = self
        while pointer is not None:
            print(f"Age: {pointer.age},  money: {pointer.money}, chosen portfolio: {pointer.portfolio}, and value: {pointer.value}")
            pointer = pointer.next
