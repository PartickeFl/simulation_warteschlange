class Task:
    """
    Repräsentiert eine Aufgabe (Task) im Simulationsmodell.
    Attribute:
        id: Eindeutige ID der Aufgabe
        arrival_time: Ankunftszeitpunkt
        finish_time: Zeitpunkt der Fertigstellung
        service_time: Bedienzeit
        sprint: Zugeordneter Sprint (optional)
        exp_alpha: Exponentiell gezogene Ankunftszeit (optional)
    """
    _id_counter: int = 1

    def __init__(self, arrival_time: float, exp_alpha: float = None) -> None:
        self.id: int = Task._id_counter
        Task._id_counter += 1
        self.arrival_time: float = arrival_time
        self.finish_time: float | None = None
        self.service_time: float | None = None
        self.sprint: int | None = None
        self.exp_alpha: float | None = exp_alpha
