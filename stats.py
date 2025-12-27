import math
from typing import List, Tuple


class Stats:
    """
    Hilfsklasse zur Berechnung von Statistikwerten (Mittelwert, Standardabweichung, Konfidenzintervall).
    """

    def __init__(self, values: List[float]) -> None:
        if not values:
            raise ValueError("Values list cannot be empty")
        self.values: List[float] = values

    def mean(self) -> float:
        """
        Berechnet den Mittelwert der Werte.
        :return: Mittelwert
        """
        return sum(self.values) / len(self.values)

    def std_dev(self) -> float:
        """
        Berechnet die Standardabweichung der Werte.
        :return: Standardabweichung
        """
        mu = self.mean()
        variance = sum((x - mu) ** 2 for x in self.values) / len(self.values)
        return math.sqrt(variance)

    def confidence_ninety_five(self) -> Tuple[float, float]:
        """
        Berechnet das 95%-Konfidenzintervall für den Mittelwert.
        :return: Untere und obere Grenze des Intervalls
        """
        quantile = 1.96  # Für 95%
        calc_mean = self.mean()
        calc_std_dev = self.std_dev()
        span = (quantile * calc_std_dev) / math.sqrt(len(self.values))
        return calc_mean - span, calc_mean + span
