import logging

from strategy1 import Strategy1
from strategy2 import Strategy2
from scenario_generator import ScenarioGenerator
from stats import Stats
from task import Task
from internal_logging import init_logging, switch_to_info


def example_run_strategy_1():
    print("Strategy 1 (FIFO):")
    s1 = Strategy1(arrival_rate=1.5, service_rate=1.0, simulation_time=10)
    print(s1.run())


def example_run_strategy_2():
    print("Strategy 2 (Sprint):")
    Task._id_counter = 1
    s2 = Strategy2(arrival_rate=1.5, service_rate=1.0, simulation_time=30, sprint_length=10)
    print(s2.run())


def analyse_strategy_1():
    print("Analyses of strategy 1")
    Task._id_counter = 1
    switch_to_info()
    s1 = Strategy1(arrival_rate=1.5, service_rate=1.0, simulation_time=240)
    scenario_generator = ScenarioGenerator(s1)
    scenario_generator.run(1000)
    for key, value_list in scenario_generator.aggregated.items():
        stats = Stats(value_list)
        logger = logging.getLogger(__name__)
        lower_bound, upper_bound = stats.confidence_ninety_five()
        logging.info(stats)
        print(key + ": " + "[" + str(lower_bound) + "; " + str(upper_bound) + "]")


if __name__ == "__main__":
    init_logging()

    #  Example runs strategy 1 & 2
    example_run_strategy_1()
    example_run_strategy_2()

    #  Analyse strategy 1
    analyse_strategy_1()
