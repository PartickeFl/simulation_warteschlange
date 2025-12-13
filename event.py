from task import Task

class Event:
    ARRIVAL = "arrival"
    DEPARTURE = "departure"
    SPRINT = "sprint"

    def __init__(self, time: int, event_type: str, data: Task | None = None):
        self.time = time
        self.type = event_type
        self.data = data

    def __lt__(self, other: Task):
        return self.time < other.time
