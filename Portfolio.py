import numpy as np


class Portfolio:
    means = 0
    variance = 0
    fees = 0
    standard_deviations = []
    correlations = [[]]

    def __init__(self, weights, means, standard_deviations, correlations, fees):
        assert np.sum(weights) == 1
        self.weights = weights
        self.means = means
        self.standard_deviations = standard_deviations
        self.correlations = correlations
        self.fees = fees
        return

    def sample_return(self):
        return round(np.dot(self.weights, self.means) * (1 - self.fees), 2)