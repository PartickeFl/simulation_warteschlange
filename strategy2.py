import random

from event import Event
from event_queue import EventQueue
from global_funcs import exp
from task import Task


class Strategy2:
    def __init__(self, arrival_rate: float, service_rate: float, simulation_time: int , sprint_length: int):
        self.alpha = arrival_rate
        self.beta = service_rate
        self.sim_time = simulation_time
        self.total_wait_time = 0

        self.T = sprint_length
        self.capacity = sprint_length

        self.buffer = []  # Tasks, die im Sprint gesammelt werden
        self.sprint_queue = []  # Tasks, die im Sprint tatsächlich bearbeitet werden
        self.server_busy = False
        self.event_queue = EventQueue()

        self.completed_tasks = []
        self.discarded_tasks = []

    def schedule_initial_events(self):
        self.event_queue.push(Event(exp(self.alpha), Event.ARRIVAL))
        self.event_queue.push(Event(self.T, Event.SPRINT))

    def run(self):
        self.schedule_initial_events()

        print("+------+-----------+-----------+-----------+-----------+--------+-----------")
        print("| id   | t_i       | e_i       | w_i       | Σ Wartezeit        | Sprint   |")
        print("+------+-----------+-----------+-----------+-----------+--------+-----------")
        while not self.event_queue.empty():
            event = self.event_queue.pop()
            current_time = event.time

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
            "avg_wait": self.average_wait_time(),
        }

    # Event handlers
    def handle_arrival(self, now):
        self.buffer.append(Task(arrival_time=now))
        self.event_queue.push(Event(now + exp(self.alpha), Event.ARRIVAL))

    def handle_sprint(self, now):
        # Sprintstart: zufällige Auswahl - Simulation einer Priorisierung
        random.shuffle(self.buffer)
        selected = self.buffer[:self.capacity]
        discarded = self.buffer[self.capacity:]

        self.sprint_queue = list(selected)
        for task in self.sprint_queue:
            task.sprint = int(now / self.T)
        self.discarded_tasks.extend(discarded)
        self.buffer = []  # Buffer leeren

        if not self.server_busy and len(self.sprint_queue) > 0:
            self.start_service(self.sprint_queue[0], now)

        # Nächsten Sprint planen
        self.event_queue.push(Event(now + self.T, Event.SPRINT))
        print("+------+-----------+ Start sprint: " + str(int(now / self.T)) + "---------------------------------+")

    def start_service(self, task, now):
        self.server_busy = True
        task.start_time = now
        service_time = exp(self.beta)
        self.event_queue.push(Event(now + service_time, Event.DEPARTURE, task))

    def handle_departure(self, event: Event, now: float):
        #  Handle departure
        task = event.data
        task.finish_time = now
        self.completed_tasks.append(task)

        #  Print information
        wait_time = task.finish_time-task.arrival_time
        self.total_wait_time += wait_time
        print(
            f"| {task.id: 4d} "
            f"| {task.arrival_time: 9.4f} "
            f"| {task.finish_time: 9.4f} "
            f"| {wait_time: 9.4f} "
            f"| {self.total_wait_time: 18.4f} "
            f"| {task.sprint: 2.0f} |"
        )

        self.sprint_queue.pop(0)
        if len(self.sprint_queue) > 0:
            self.start_service(self.sprint_queue[0], now)
        else:
            self.server_busy = False

    def average_wait_time(self):
        if not self.completed_tasks:
            return 0
        waits = [t.finish_time - t.arrival_time for t in self.completed_tasks]
        return sum(waits) / len(waits)
