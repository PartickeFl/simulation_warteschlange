import math


class Stats:
    def __init__(self, values):
        if not values:
            raise ValueError("Values list cannot be empty")
        self.values = values

    def mean(self):
        return sum(self.values) / len(self.values)

    def std_dev(self):
        mu = self.mean()
        variance = sum((x - mu) ** 2 for x in self.values) / len(self.values)
        return math.sqrt(variance)

    def confidence_ninety_five(self):
        quantile = 1.96  # For 95%
        calc_mean = self.mean()
        calc_std_dev = self.std_dev()
        span = (quantile * calc_std_dev) / math.sqrt(len(self.values))
        return calc_mean - span, calc_mean + span
