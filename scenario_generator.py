import copy
from collections import defaultdict
from typing import Any, Callable, Dict, List


class ScenarioGenerator:
    """
    Führt mehrere Simulationen eines Szenarios aus und aggregiert die Ergebnisse.
    """

    def __init__(self, scenario_class: Any) -> None:
        """
        :param scenario_class: Ein aufrufbares Klassenobjekt, dessen run()-Methode ein Dict zurückgibt
        """
        self.scenario_class: Any = scenario_class
        self.aggregated: Dict[str, List[Any]] = defaultdict(list)

    def run(self, times: int) -> Dict[str, List[Any]]:
        """
        Führt das Szenario mehrfach aus und aggregiert die Ergebnisse.
        :param times: Anzahl der Durchläufe
        :return: Aggregierte Ergebnisse als Dict
        """
        for _ in range(times):
            temp_scenario = copy.deepcopy(self.scenario_class)  # Sicherstellen, dass jedes Mal ein frisches Objekt verwendet wird
            result = temp_scenario.run()
            for key, value in result.items():
                self.aggregated[key].append(value)

        self.aggregated = dict(self.aggregated)

        return self.aggregated
