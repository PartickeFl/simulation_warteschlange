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
