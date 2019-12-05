import numpy as np
import numpy.random as nr

EPS = 0.0001


class Portfolio:

    # The means and covariance matrix should be normal and not log based.
    def __init__(self, weights, means, covariance_matrix, fees):
        assert np.sum(weights) > 1 - EPS
        assert np.sum(weights) < 1 + EPS

        self.weights = weights
        self.means = means
        self.covariance_matrix = covariance_matrix
        self.fees = fees

        return

    # The sampled return is log based, round 3 decimal points.
    def sample_return(self):
        multivariate_normal = nr.multivariate_normal(self.means, self.covariance_matrix)
        multivariate_log_normal = np.exp(multivariate_normal) - 1

        returns = round(np.dot(self.weights, multivariate_log_normal) * (1 - self.fees), 3)
        return returns
