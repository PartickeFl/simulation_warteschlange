"""
Modul: Strategie 1 – Abarbeitung auf Zuruf

Dieses Modul implementiert eine ereignisbasierte Simulation eines Einkanal-Bedienungssystems
mit einer FIFO-Warteschlange.
Ankommende Aufgaben (Tasks) werden in der Reihenfolge ihres Eintreffens bearbeitet,
ohne Priorisierung oder Unterbrechung.
Ereignisbasierte Simulation eines Einkanal-Bedienungssystems (M/M/1, FIFO) mit ASCII-Ausgabe pro Task-Ankunft.

Annahmen und Eigenschaften:
- Die Ankunftszeiten der Tasks folgen einer Exponentialverteilung mit Rate alpha (Poisson-Prozess).
- Die Bedienzeiten sind ebenfalls exponentialverteilt mit Rate beta.
- Es existiert genau eine Ressource, d.h. ein Kanal.
- Ist der Kanal frei, wird der zuerst eingetroffene Task sofort bedient.
- Ereignisse (Ankunft und Abgang) werden über eine Ereigniswarteschlange zeitlich sortiert verarbeitet.
- Die Simulation läuft bis zur vorgegebenen Simulationszeit.

Ausgaben der Simulation:
- Anzahl der vollständig bearbeiteten Tasks
- Länge der Warteschlange am Ende der Simulation
- Mittlere Wartezeit
- Mittlere Schlangenlänge
- Auslastungsgrad
"""
import logging
from typing import List
from event import Event
from event_queue import EventQueue
from task import Task
from global_funcs import exp


class Strategy1:
    """
    Strategie 1: FIFO-Simulation eines Einkanal-Bedienungssystems (M/M/1).
    """
    def __init__(self, arrival_rate: float, service_rate: float, simulation_time: float) -> None:
        """
        Initialisiert die Simulationsparameter und Zustandsvariablen.
        :param arrival_rate: Ankunftsrate (alpha)
        :param service_rate: Bedienrate (beta)
        :param simulation_time: Maximale Simulationszeit
        """
        self.alpha: float = arrival_rate  # Ankunftsrate
        self.beta: float = service_rate   # Bedienrate
        self.sim_time: float = simulation_time  # Simulationszeit

        self.last_event_time: float = 0.0  # Zeitpunkt des letzten Events
        self.area_queue: float = 0.0       # Fläche unter der Warteschlangenlänge (für Mittelwert)
        self.busy_time: float = 0.0        # Gesamte Bedienzeit

        self.queue: List[Task] = []        # FIFO-Warteschlange
        self.server_busy: bool = False     # Status des Servers
        self.event_queue: EventQueue = EventQueue()  # Ereigniswarteschlange

        self.completed_tasks: List[Task] = []  # Liste der abgeschlossenen Tasks

        # Für Tabellen-Ausgabe und Statistik
        self.last_arrival_time: float = 0.0
        self.total_service_time: float = 0.0
        self.total_wait_time: float = 0.0
        self.logger = logging.getLogger(__name__)

    def schedule_initial_events(self) -> None:
        """
        Plant das erste Ankunftsereignis.
        """
        first_arrival: float = exp(self.alpha)
        self.event_queue.push(Event(int(first_arrival), Event.ARRIVAL))  # Typkonvertierung zu int

    def print(self, text: str) -> None:
        """
        Gibt Text als Debug-Log aus (für Tabellen-Ausgabe).
        :param text: Textzeile
        """
        self.logger.debug(text)

    def run(self) -> dict:
        """
        Führt die Simulation aus und berechnet die Kennzahlen.
        :return: Dictionary mit Ergebnissen (Anzahl, mittlere Wartezeit, etc.)
        """
        self.schedule_initial_events()

        # Tabellenkopf für Debug-Ausgabe
        self.print("+------+-----------+-----------+-----------+-----------+---------+----------------------+--------------------+")
        self.print("| id   | a_i       | t_i       | b_i       | e_i       | w_i     | Σ Bedienzeit         | Σ Wartezeit        |")
        self.print("+------+-----------+-----------+-----------+-----------+---------+----------------------+--------------------+")

        last_task_e_i: float = 0.0  # Zeitpunkt des letzten Task-Endes
        while not self.event_queue.empty():
            event: Event = self.event_queue.pop()
            current_time: float = event.time

            if current_time > self.sim_time:
                break

            time_delta: float = current_time - self.last_event_time
            self.area_queue += len(self.queue) * time_delta
            if self.server_busy:
                self.busy_time += time_delta

            self.last_event_time = current_time

            if event.type == Event.ARRIVAL:
                last_task_e_i = self.handle_arrival(current_time, last_task_e_i)
            elif event.type == Event.DEPARTURE:
                self.handle_departure(event, current_time)

        # Ergebnisberechnung
        num_completed: int = len(self.completed_tasks)
        queue_len_end: int = len(self.queue)
        avg_wait: float = self.total_wait_time / (queue_len_end + num_completed) if (queue_len_end + num_completed) > 0 else 0.0
        avg_queue_len: float = self.total_wait_time / last_task_e_i if last_task_e_i > 0 else 0.0
        utilization: float = self.total_service_time / last_task_e_i if last_task_e_i > 0 else 0.0
        return {
            "completed": num_completed,
            "queue_len_end": queue_len_end,
            "avg_wait": avg_wait,
            "avg_queue_len": avg_queue_len,
            "utilization": utilization
        }

    def handle_arrival(self, now: float, last_task_e_i: float) -> float:
        """
        Behandelt ein Ankunftsereignis: Task erzeugen, Bedienzeit ziehen, nächste Ankunft planen.
        :param now: Aktuelle Simulationszeit
        :param last_task_e_i: Zeitpunkt des letzten Task-Endes
        :return: Neuer Zeitpunkt des aktuellen Task-Endes
        """
        a_i: float = now - self.last_arrival_time  # Zwischenankunftszeit
        self.last_arrival_time = now

        task: Task = Task(arrival_time=now)
        task.service_time = exp(self.beta)  # Bedienzeit ziehen
        b_i: float = task.service_time
        self.queue.append(task)

        # Nächste Ankunft planen
        self.event_queue.push(Event(now + exp(self.alpha), Event.ARRIVAL))

        # Zeitpunkt, zu dem dieser Task fertig ist
        task_e_i: float = max(task.arrival_time, last_task_e_i) + b_i
        if not self.server_busy:
            self.start_service(task, now)

        # Kumulative Zeiten für Statistik
        self.total_service_time += b_i
        current_wait: float = max(0.0, last_task_e_i - task.arrival_time)  # 0.0 statt 0 für float
        self.total_wait_time += current_wait

        # Tabellenzeile für Debug-Ausgabe
        self.print(
            f"| {task.id: 4d} "
            f"| {a_i: 9.4f} "
            f"| {task.arrival_time: 9.4f} "
            f"| {b_i: 9.4f} "
            f"| {task_e_i: 9.4f} "
            f"| {current_wait: 9.4f} "
            f"| {self.total_service_time: 20.4f} "
            f"| {self.total_wait_time: 18.4f} |"
        )

        return task_e_i

    def start_service(self, task: Task, now: float) -> None:
        """
        Startet die Bedienung eines Tasks und plant das Abgangsereignis.
        :param task: Zu bedienender Task
        :param now: Aktuelle Simulationszeit
        """
        self.server_busy = True
        completion_event: Event = Event(
            int(now + task.service_time),  # Typkonvertierung zu int
            Event.DEPARTURE,
            task
        )
        self.event_queue.push(completion_event)

    def handle_departure(self, event: Event, now: float) -> None:
        """
        Behandelt ein Abgangsereignis: Task abschließen, ggf. nächsten Task starten.
        :param event: Abgangsereignis
        :param now: Aktuelle Simulationszeit
        """
        task: Task = event.data
        task.finish_time = now
        self.completed_tasks.append(task)

        self.queue.pop(0)
        if len(self.queue) > 0:
            next_task: Task = self.queue[0]
            self.start_service(next_task, now)
        else:
            self.server_busy = False
