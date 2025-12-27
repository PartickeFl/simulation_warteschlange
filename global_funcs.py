import random


def exp(rate: float) -> float:
    """
    Gibt eine Zufallszahl aus einer Exponentialverteilung mit gegebener Rate zurück.
    :param rate: Rateparameter (lambda) der Exponentialverteilung
    :return: Zufallswert entsprechend der Exponentialverteilung
    """
    return random.expovariate(rate)
