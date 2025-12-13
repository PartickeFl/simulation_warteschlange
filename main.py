from strategy1 import Strategy1
from strategy2 import Strategy2
from task import Task

# -------------------------------------------------------------
# Beispielausführung
# -------------------------------------------------------------
if __name__ == "__main__":
    for i in range(1000):
        print("Szenario 1 (FIFO):")
        s1 = Strategy1(arrival_rate=1.5, service_rate=1.0, simulation_time=360)
        print(s1.run())

        print("\nSzenario 2 (Sprint):")
        Task._id_counter = 1
        s2 = Strategy2(arrival_rate=1.5, service_rate=1.0, simulation_time=360, sprint_length=10)
        print(s2.run())
