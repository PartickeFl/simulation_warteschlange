"""
Modul: Strategie 2 – Sprintplanung mit zufälliger Auswahl

Dieses Modul implementiert eine ereignisbasierte Simulation eines Einkanal-Bedienungssystems,
bei dem Aufgaben (Tasks) in festen Zeitintervallen (Sprints) gesammelt und anschließend
zufällig zur Bearbeitung ausgewählt werden. Die Anzahl der pro Sprint bearbeiteten Aufgaben
ist durch eine Kapazitätsgrenze beschränkt. Nicht ausgewählte Aufgaben werden verworfen.

Annahmen und Eigenschaften:
- Die Ankunftszeiten der Tasks folgen einer Exponentialverteilung mit Rate alpha (Poisson-Prozess).
- Die Bedienzeiten sind ebenfalls exponentialverteilt mit Rate beta.
- Aufgaben werden in einem Buffer gesammelt und zu festen Zeitpunkten (Sprint-Start) zufällig ausgewählt.
- Pro Sprint können maximal T Aufgaben bearbeitet werden (Kapazitätsgrenze).
- Nicht ausgewählte Aufgaben eines Sprints werden verworfen.
- Die Bearbeitung erfolgt sequentiell, ohne Unterbrechung, innerhalb des Sprints.
- Die Simulation läuft bis zur vorgegebenen Simulationszeit.

Ausgaben der Simulation:
- Anzahl der vollständig bearbeiteten Tasks
- Anzahl der verworfenen Tasks
- Mittlere Wartezeit der bearbeiteten Tasks
"""
import random
import logging
from typing import List

from event import Event
from event_queue import EventQueue
from global_funcs import exp
from task import Task


class Strategy2:
    """
    Strategie 2: Sprints mit zufälliger Auswahl und Kapazitätsgrenze.
    Aufgaben werden in Sprints gesammelt und dann zufällig ausgewählt und bearbeitet.
    """
    def __init__(self, arrival_rate: float, service_rate: float, simulation_time: int, sprint_length: int) -> None:
        """
        Initialisiert die Simulationsparameter und Zustandsvariablen.
        :param arrival_rate: Ankunftsrate (alpha)
        :param service_rate: Bedienrate (beta)
        :param simulation_time: Maximale Simulationszeit
        :param sprint_length: Länge eines Sprints (Kapazität und Intervall)
        """
        self.alpha: float = arrival_rate
        self.beta: float = service_rate
        self.sim_time: int = simulation_time
        self.total_wait_time: float = 0.0  # Typ float für Wartezeit, auch wenn sim_time int ist

        self.T: int = sprint_length
        self.capacity: int = sprint_length

        self.buffer: List[Task] = []  # Tasks, die im Sprint gesammelt werden
        self.sprint_queue: List[Task] = []  # Tasks, die im Sprint tatsächlich bearbeitet werden
        self.server_busy: bool = False
        self.event_queue: EventQueue = EventQueue()

        self.completed_tasks: List[Task] = []
        self.discarded_tasks: List[Task] = []
        self.logger = logging.getLogger(__name__)

    def print(self, text: str) -> None:
        """
        Gibt Text als Debug-Log aus (für Tabellen-Ausgabe).
        :param text: Textzeile
        """
        self.logger.debug(text)

    def schedule_initial_events(self) -> None:
        """
        Plant das erste Ankunfts- und Sprint-Ereignis.
        """
        # Zeitpunkte müssen als int übergeben werden
        self.event_queue.push(Event(int(exp(self.alpha)), Event.ARRIVAL))
        self.event_queue.push(Event(self.T, Event.SPRINT))

    def run(self) -> dict:
        """
        Führt die Simulation aus und berechnet die Kennzahlen.
        :return: Dictionary mit Ergebnissen (Anzahl, verworfene Tasks, mittlere Wartezeit)
        """
        self.schedule_initial_events()

        self.print("+------+-----------+-----------+-----------+-----------+-----------+--------------------+----------+")
        self.print("| id   | a_i       | t_i       | b_i       | e_i       | w_i       | Σ Wartezeit        | Sprint   |")
        self.print("+------+-----------+-----------+-----------+-----------+-----------+--------------------+----------+")
        while not self.event_queue.empty():
            event: Event = self.event_queue.pop()
            current_time: float = event.time

            if current_time > self.sim_time:
                break

            if event.type == Event.ARRIVAL:
                self.handle_arrival(current_time)
            elif event.type == Event.SPRINT:
                self.handle_sprint(current_time)
            elif event.type == Event.DEPARTURE:
                self.handle_departure(event, current_time)

        return {
            "completed": len(self.completed_tasks),
            "discarded": len(self.discarded_tasks),
            "avg_wait": self.total_wait_time / len(self.completed_tasks) if self.completed_tasks else 0.0
        }

    # Event handlers
    def handle_arrival(self, now: float) -> None:
        """
        Behandelt ein Ankunftsereignis: Task erzeugen, nächste Ankunft planen.
        :param now: Aktuelle Simulationszeit
        """
        exp_alpha: float = exp(self.alpha)
        self.buffer.append(Task(arrival_time=now, exp_alpha=exp_alpha))
        self.event_queue.push(Event(now + exp_alpha, Event.ARRIVAL))

    def handle_sprint(self, now: float) -> None:
        """
        Behandelt ein Sprint-Ereignis: Auswahl und Start der Tasks im Sprint.
        :param now: Aktuelle Simulationszeit
        """
        random.shuffle(self.buffer)
        selected: List[Task] = self.buffer[:self.capacity]
        discarded: List[Task] = self.buffer[self.capacity:]

        self.sprint_queue = list(selected)
        for task in self.sprint_queue:
            task.sprint = int(now / self.T)
        self.discarded_tasks.extend(discarded)
        self.buffer = []  # Buffer leeren

        if not self.server_busy and len(self.sprint_queue) > 0:
            self.start_service(self.sprint_queue[0], now)

        # Nächsten Sprint planen (Zeitpunkt als int)
        self.event_queue.push(Event(int(now + self.T), Event.SPRINT))
        self.print("+------+-----------+ Start sprint: " + str(int(now / self.T)) + "---------------------------------+")

    def start_service(self, task: Task, now: float) -> None:
        """
        Startet die Bedienung eines Tasks und plant das Abgangsereignis.
        :param task: Zu bedienender Task
        :param now: Aktuelle Simulationszeit
        """
        self.server_busy = True
        task.start_time = now
        service_time: float = exp(self.beta)
        task.service_time = service_time
        # Zeitpunkte als int übergeben
        self.event_queue.push(Event(now + service_time, Event.DEPARTURE, task))

    def handle_departure(self, event: Event, now: float) -> None:
        """
        Behandelt ein Abgangsereignis: Task abschließen, ggf. nächsten Task starten.
        :param event: Abgangsereignis
        :param now: Aktuelle Simulationszeit
        """
        task: Task = event.data
        task.finish_time = now
        self.completed_tasks.append(task)

        # Wartezeit berechnen und Statistik aktualisieren
        wait_time: float = task.finish_time - task.arrival_time - task.service_time
        self.total_wait_time += wait_time
        self.print(
            f"| {task.id: 4d} "
            f"| {task.exp_alpha: 9.4f} "
            f"| {task.arrival_time: 9.4f} "
            f"| {task.service_time: 9.4f} "
            f"| {task.finish_time: 9.4f} "
            f"| {wait_time: 9.4f} "
            f"| {self.total_wait_time: 18.4f} "
            f"| {task.sprint: 2.0f} |"
        )
        if len(self.sprint_queue) > 0:
            self.sprint_queue.pop(0)
            if len(self.sprint_queue) > 0:
                self.start_service(self.sprint_queue[0], now)
            else:
                self.server_busy = False
        else:
            self.server_busy = False
