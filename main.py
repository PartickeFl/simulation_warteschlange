from strategy1 import Strategy1
from strategy2 import Strategy2
from task import Task


def example_run_scenario_1():
    print("Szenario 1 (FIFO):")
    s1 = Strategy1(arrival_rate=1.5, service_rate=1.0, simulation_time=30)
    print(s1.run())


def example_run_scenario_2():
    print("Szenario 2 (Sprint):")
    Task._id_counter = 1
    s2 = Strategy2(arrival_rate=1.5, service_rate=1.0, simulation_time=30, sprint_length=10)
    print(s2.run())


if __name__ == "__main__":
    example_run_scenario_1()
    example_run_scenario_2()
