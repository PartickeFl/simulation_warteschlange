import heapq

class EventQueue:
    def __init__(self, events=None):
        # If you already have events, use heapify to make it a heap
        self.queue = events if events else []
        if self.queue:
            heapq.heapify(self.queue)

    def push(self, event):
        heapq.heappush(self.queue, event)

    def pop(self):
        return heapq.heappop(self.queue)

    def empty(self):
        return len(self.queue) == 0

    def max(self):
        if self.queue:
            return max(self.queue)
        return None
