import heapq
from typing import List, Optional
from event import Event

class EventQueue:
    """
    Prioritätswarteschlange für Events, basierend auf einem Heap.
    Ermöglicht effizientes Einfügen und Entfernen von Events nach Zeit.
    """
    def __init__(self, events: Optional[List[Event]] = None) -> None:
        """
        Initialisiert die EventQueue. Optional kann eine Liste von Events übergeben werden.
        :param events: Optionale Liste von Event-Objekten
        """
        self.queue: List[Event] = events if events else []
        if self.queue:
            heapq.heapify(self.queue)  # Heap-Eigenschaft sicherstellen

    def push(self, event: Event) -> None:
        """
        Fügt ein Event in die Warteschlange ein.
        :param event: Das einzufügende Event
        """
        heapq.heappush(self.queue, event)

    def pop(self) -> Event:
        """
        Entfernt und gibt das Event mit der kleinsten Zeit zurück.
        :return: Event mit der kleinsten Zeit
        """
        return heapq.heappop(self.queue)

    def empty(self) -> bool:
        """
        Prüft, ob die Warteschlange leer ist.
        :return: True, wenn leer, sonst False
        """
        return len(self.queue) == 0

    def max(self) -> Optional[Event]:
        """
        Gibt das Event mit der größten Zeit zurück (ohne zu entfernen).
        :return: Event mit größter Zeit oder None, falls leer
        """
        if self.queue:
            return max(self.queue)
        return None
