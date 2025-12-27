from task import Task
from typing import Optional, Any

class Event:
    """
    Repräsentiert ein Ereignis im Simulationsmodell.
    Typen: Ankunft, Abgang, Sprint.
    time: Zeitpunkt des Ereignisses (z.B. Simulationszeit)
    type: Art des Ereignisses (z.B. 'arrival', 'departure', 'sprint')
    data: Optionales Zusatzobjekt, z.B. ein Task
    """
    ARRIVAL: str = "arrival"
    DEPARTURE: str = "departure"
    SPRINT: str = "sprint"

    def __init__(self, time: float, event_type: str, data: Optional[Task] = None) -> None:
        self.time: float = time  # Zeitpunkt des Ereignisses
        self.type: str = event_type  # Typ des Ereignisses
        self.data: Optional[Task] = data  # Zusatzdaten, z.B. Task-Objekt

    def __lt__(self, other: Any) -> bool:
        """
        Vergleichsfunktion für die Sortierung von Events nach Zeit.
        Ermöglicht z.B. die Nutzung in einer Prioritätswarteschlange.
        """
        return self.time < other.time
