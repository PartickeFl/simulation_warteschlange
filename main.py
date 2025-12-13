from strategy1 import Strategy1
from strategy2 import Strategy2

# -------------------------------------------------------------
# Beispielausführung
# -------------------------------------------------------------
if __name__ == "__main__":
    print("Szenario 1 (FIFO):")
    s1 = Strategy1(arrival_rate=1.5, service_rate=1.0, simulation_time=360)
    print(s1.run())

    print("\nSzenario 2 (Sprint):")
    s2 = Strategy2(arrival_rate=1.0, service_rate=1.0,
                   simulation_time=1000, sprint_length=10, sprint_capacity=10)
    print(s2.run())
