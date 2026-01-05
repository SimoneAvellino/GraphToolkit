import random
from distributions.strategy import DistributionStratetegy


class GaussianDistribution(DistributionStratetegy):

    def __init__(self, mean: float, stddev: float):
        self.mean = mean
        self.stddev = stddev

    def get(self):

        return random.gauss(self.mean, self.stddev)
