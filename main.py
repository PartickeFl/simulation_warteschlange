import logging
from typing import Dict, List

from strategy1 import Strategy1
from strategy2 import Strategy2
from scenario_generator import ScenarioGenerator
from stats import Stats
from task import Task
from curve_family import CurveFamily
from internal_logging import init_logging, switch_to_info


def example_run_strategy_1() -> None:
    """
    3.1.1 Beispielhafte Auswertung Strategie 1
    Ermittlung der Ergebnisse für Kapitel 3.1.1, wobei auf Grund der Zufallsvariablen
    sich die Ergebnisse unterscheiden können. Es wurde ein Lauf zur Auswertung beispielhaft
    herangezogen.
    """
    print("Strategy 1 (FIFO):")
    s1: Strategy1 = Strategy1(arrival_rate=1.5, service_rate=1.0, simulation_time=10)
    print(s1.run())


def analysis_strategy_1() -> None:
    """
    3.1.2	Output-Metriken mit Konfidenzintervallen
    Ermittlung der Output-Metriken mit Konfidenzintervallen, wobei auf Grund der Zufallsvariablen
    sich die Ergebnisse unterscheiden können. Es wir die Strategie N = 10000 mit Hilfe eines
    Szenariongenerators durchgeführt und anschließend die Konfidenzintervalle mit Mittelwerten ermittelt.
    """
    print("Analysis of strategy 1")
    Task._id_counter = 1
    switch_to_info()
    s1: Strategy1 = Strategy1(arrival_rate=1.5, service_rate=1.0, simulation_time=240)
    scenario_generator: ScenarioGenerator = ScenarioGenerator(s1)
    logging.info(scenario_generator.run(10000))
    for key, value_list in scenario_generator.aggregated.items():
        stats: Stats = Stats(value_list)
        lower_bound, upper_bound = stats.confidence_ninety_five()
        print(f"{key}: [{lower_bound}; {upper_bound}]")


def example_run_strategy_2() -> None:
    """
    3.2.1 Beispielhafte Auswertung Strategie 2
    Ermittlung der Ergebnisse für Kapitel 3.2.1, wobei auf Grund der Zufallsvariablen
    sich die Ergebnisse unterscheiden können. Es wurde ein Lauf zur Auswertung beispielhaft
    herangezogen.
    """
    print("Strategy 2 (Sprint):")
    Task._id_counter = 1
    s2: Strategy2 = Strategy2(arrival_rate=1.5, service_rate=1.0, simulation_time=30, sprint_length=10)
    print(s2.run())


def analysis_strategy_2() -> None:
    """
    3.2.2	Output-Metriken mit Konfidenzintervallen
    Ermittlung der Output-Metriken mit Konfidenzintervallen, wobei auf Grund der Zufallsvariablen
    sich die Ergebnisse unterscheiden können. Es wir die Strategie N = 10000 mit Hilfe eines
    Szenariongenerators durchgeführt und anschließend die Konfidenzintervalle mit Mittelwerten ermittelt.
    """
    print("Analysis of strategy 2")
    Task._id_counter = 1
    switch_to_info()
    s2: Strategy2 = Strategy2(arrival_rate=1.5, service_rate=1.0, simulation_time=240, sprint_length=10)
    scenario_generator: ScenarioGenerator = ScenarioGenerator(s2)
    logging.info(scenario_generator.run(10000))
    for key, value_list in scenario_generator.aggregated.items():
        stats: Stats = Stats(value_list)
        lower_bound, upper_bound = stats.confidence_ninety_five()
        print(f"{key}: [{lower_bound}; {upper_bound}]")


def analyse_strategy_2_params() -> None:
    """
    3.2.3 Vergleich für verschiedene Sprintintervalle und Ankunftsraten, es werden verschiedene
    Ankunfstraten sowie verschiedene Sprintdauern gesetzt. Die verworfenen Tasks sowie die
    mittleren Wartezeiten werden in Diagrammen abgespeichert.
    """
    #  Disable logging
    switch_to_info()
    Task._id_counter = 1
    result_dict: Dict[int, Dict[str, List[float]]] = {}
    list_alpha: List[float] = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8]

    # Berechnung der Ergebnisse für verschiedene Sprintlängen und Ankunftsraten
    for T in [5, 10, 20]:
        result_dict[T] = {'discarded': [], 'avg_wait': []}
        for alpha in list_alpha:
            s2: Strategy2 = Strategy2(arrival_rate=alpha, service_rate=1.0, simulation_time=240, sprint_length=T)
            scenario_generator: ScenarioGenerator = ScenarioGenerator(s2)
            logging.info(f"Scenario: alpha: {alpha}; T: {T}")
            logging.info(scenario_generator.run(10000))
            stats_discarded: Stats = Stats(scenario_generator.aggregated["discarded"])
            stats_avg_wait: Stats = Stats(scenario_generator.aggregated["avg_wait"])
            result_dict[T]['discarded'].append(stats_discarded.mean())
            result_dict[T]['avg_wait'].append(stats_avg_wait.mean())
    print(result_dict)

    curve_titles: List[str] = ["T = 5", "T = 10", "T = 20"]
    y1: List[List[float]] = [result_dict[5]['discarded'], result_dict[10]['discarded'], result_dict[20]['discarded']]
    y2: List[List[float]] = [result_dict[5]['avg_wait'], result_dict[10]['avg_wait'], result_dict[20]['avg_wait']]
    x: List[List[float]] = [list_alpha, list_alpha, list_alpha]

    # Speichern der Diagramme für verworfene Tasks
    curves: CurveFamily = CurveFamily(x, y1)
    curves.save(
        title="Verworfene Tasks für verschiedene Sprintdauern T",
        curve_titles=curve_titles,
        filename="discarded.png",
        x_label="alpha/beta",
        y_label="Verworfene Tasks"
    )

    # Speichern der Diagramme für mittlere Wartezeiten
    curves = CurveFamily(x, y2)
    curves.save(
        title="Mittlere Wartezeit für verschiedene Sprintdauern T",
        curve_titles=curve_titles,
        filename="avg_wait.png",
        x_label="alpha/beta",
        y_label="Mittlere Wartezeit"
    )


if __name__ == "__main__":
    init_logging()
    #example_run_strategy_1()   # Abschnitt 3.1.1
    #analysis_strategy_1()      # Abschnitt 3.1.2
    #example_run_strategy_2()   # Abschnitt 3.2.1
    analysis_strategy_2()      # Abschnitt 3.2.2
    #analyse_strategy_2_params() # Abschnitt 3.2.3
