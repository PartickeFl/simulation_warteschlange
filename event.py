class Event:
    ARRIVAL = "arrival"
    DEPARTURE = "departure"
    SPRINT = "sprint"

    def __init__(self, time, event_type, data=None):
        self.time = time
        self.type = event_type
        self.data = data

    def __lt__(self, other):
        return self.time < other.time