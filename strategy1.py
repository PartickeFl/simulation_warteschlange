"""
Modul: Strategy1 – Abarbeitung auf Zuruf

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

from event import Event
from event_queue import EventQueue
from task import Task
from global_funcs import exp


class Strategy1:
    def __init__(self, arrival_rate, service_rate, simulation_time):
        self.alpha = arrival_rate
        self.beta = service_rate
        self.sim_time = simulation_time

        self.last_event_time = 0.0
        self.area_queue = 0.0
        self.busy_time = 0.0

        self.queue = []
        self.server_busy = False
        self.event_queue = EventQueue()

        self.completed_tasks = []

        # Für Tabellen-Ausgabe
        self.last_arrival_time = 0.0
        self.total_service_time = 0.0
        self.total_wait_time = 0.0

    def schedule_initial_events(self):
        first_arrival = exp(self.alpha)
        self.event_queue.push(Event(first_arrival, Event.ARRIVAL))

    def run(self):
        self.schedule_initial_events()
        current_time = 0.0

        # Tabellenkopf
        print("+------+-----------+-----------+-----------+-----------+---------+----------------------+--------------------+")
        print("| id   | a_i       | t_i       | b_i       | e_i       | w_i     | Σ Bedienzeit         | Σ Wartezeit        |")
        print("+------+-----------+-----------+-----------+-----------+---------+----------------------+--------------------+")

        last_task_e_i = 0
        while not self.event_queue.empty():
            event = self.event_queue.pop()
            current_time = event.time

            if current_time > self.sim_time:
                break

            time_delta = current_time - self.last_event_time
            self.area_queue += len(self.queue) * time_delta
            if self.server_busy:
                self.busy_time += time_delta

            self.last_event_time = current_time

            if event.type == Event.ARRIVAL:
                last_task_e_i = self.handle_arrival(current_time, last_task_e_i)
            elif event.type == Event.DEPARTURE:
                self.handle_departure(event, current_time)

        return {
            "completed": len(self.completed_tasks),
            "queue_len_end": len(self.queue),
            "avg_wait": self.total_wait_time / (len(self.queue) + len(self.completed_tasks)),
            "avg_queue_len": self.total_wait_time / last_task_e_i,
            "utilization": self.total_service_time / last_task_e_i
        }

    def handle_arrival(self, now, last_task_e_i):
        # Zwischenankunftszeit
        a_i = now - self.last_arrival_time
        self.last_arrival_time = now

        # Task erzeugen
        task = Task(arrival_time=now)

        # Bediendauer einmal ziehen
        task.service_time = exp(self.beta)
        b_i = task.service_time
        self.queue.append(task)

        # Nächste Ankunft planen
        self.event_queue.push(Event(now + exp(self.alpha), Event.ARRIVAL))

        # Zeitpunkt des Bedienenden des i-ten Kunden
        task_e_i = max(task.arrival_time, last_task_e_i) + b_i
        if not self.server_busy:
            self.start_service(task, now)

        # Kumulative Zeiten
        self.total_service_time += b_i
        current_wait = max(0, last_task_e_i - task.arrival_time)
        self.total_wait_time += current_wait

        # Tabellenzeile
        print(
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

    def start_service(self, task, now):
        self.server_busy = True
        completion_event = Event(
            now + task.service_time,
            Event.DEPARTURE,
            task
        )
        self.event_queue.push(completion_event)

    def handle_departure(self, event, now):
        task = event.data
        task.finish_time = now
        self.completed_tasks.append(task)

        self.queue.pop(0)
        if len(self.queue) > 0:
            next_task = self.queue[0]
            self.start_service(next_task, now)
        else:
            self.server_busy = False
