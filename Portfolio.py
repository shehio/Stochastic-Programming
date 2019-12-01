import numpy as np
import numpy.random as nr

EPS = 0.0001


class Portfolio:

    def __init__(self, weights, means, standard_deviations, correlations, fees):
        assert np.sum(weights) > 1 - EPS
        assert np.sum(weights) < 1 + EPS
        self.weights = weights
        self.means = means
        self.standard_deviations = standard_deviations
        self.correlations = correlations
        self.fees = fees
        self.std_diag = np.diag(self.standard_deviations)
        self.covariance = self.std_diag * self.correlations * self.std_diag
        self.mu_log = np.log(self.means)

        return

    def sample_return(self):
        multivariate_normal = nr.multivariate_normal(self.means, self.covariance)
        multivariate_log_normal = np.exp(multivariate_normal) - 1  # He is saying there should be a -1 here.

        returns = round(np.dot(self.weights, multivariate_log_normal) * (1 - self.fees), 3)
        return returns
