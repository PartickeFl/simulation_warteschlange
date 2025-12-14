class Task:
    _id_counter = 1

    def __init__(self, arrival_time, exp_alpha=None):
        self.id = Task._id_counter
        Task._id_counter += 1
        self.arrival_time = arrival_time
        self.finish_time = None
        self.service_time = None
        self.sprint = None
        self.exp_alpha = exp_alpha
