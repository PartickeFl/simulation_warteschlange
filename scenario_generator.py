from collections import defaultdict


class ScenarioGenerator:
    def __init__(self, scenario_class):
        """
        scenario_class: a callable class which run function returns a dict
        """
        self.scenario_class = scenario_class

    def run(self, times):
        aggregated = defaultdict(list)

        for _ in range(times):
            result = self.scenario_class.run()
            for key, value in result.items():
                aggregated[key].append(value)

        return dict(aggregated)
