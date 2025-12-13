class Task:
    _id_counter = 1

    def __init__(self, arrival_time):
        self.id = Task._id_counter
        Task._id_counter += 1
        self.arrival_time = arrival_time
        self.start_time = None
        self.finish_time = None
        self.service_time = None
