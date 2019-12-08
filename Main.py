import PortfolioFactory as PortfolioFactory
import ValueFunctionCalculator as ValueFunctionCalculator
import Client as Client
import time


class Solution:

    def __init__(self, step, simulation_number, money_lower_bound, money_upper_bound, clients):
        self.step = step
        self.money_lower_bound = money_lower_bound
        self.money_upper_bound = money_upper_bound
        self.portfolios = PortfolioFactory.PortfolioFactory().get_available_portfolios()
        self.state_trajectory = {}
        self.value_function_calculator = ValueFunctionCalculator.ValueFunctionCalculator(
            self.money_lower_bound,
            self.money_upper_bound,
            self.portfolios,
            step,
            simulation_number)
        for client in clients:
            self.state_trajectory[client] = self.value_function_calculator.populate_value_function(client)
        return


print(f"Starting the program...")

Amy = Client.Client('Amy', 50, 67, 1000)
Bob = Client.Client('Bob', 54, 67, 900)
Carla = Client.Client('Carla', 54, 67, 500)
Darrin = Client.Client('Darrin', 57, 67, 1500)
Eric = Client.Client('Eric', 62, 67, 1200)
Francine = Client.Client('Francine', 65, 67, 1600)
clients = [Amy, Bob, Carla, Darrin, Eric, Francine]

start = time.time()
solution = Solution(
    step=10,
    simulation_number=1000,
    money_lower_bound=0,
    money_upper_bound=3000,
    clients=clients)
end = time.time()
print(f"Total execution time in minutes: {(end - start) / 60}")

for client in clients:
    print(f"Client: {client.name}")
    for i, helper in enumerate(solution.state_trajectory[client]):  # 1 helper for a portfolio
        print(f"For portfolio {i + 1}")
        helper.print()
