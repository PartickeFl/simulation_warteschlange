import copy
from collections import defaultdict


class ScenarioGenerator:
    def __init__(self, scenario_class):
        """
        scenario_class: a callable class which run function returns a dict
        """
        self.scenario_class = scenario_class
        self.aggregated = defaultdict(list)

    def run(self, times):
        for _ in range(times):
            temp_scenario = copy.deepcopy(self.scenario_class)  # Make sure that it starts always from the beginning
            result = temp_scenario.run()
            for key, value in result.items():
                self.aggregated[key].append(value)

        self.aggregated = dict(self.aggregated)

        return self.aggregated
