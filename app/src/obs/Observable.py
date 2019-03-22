from abc import abstractmethod
from obs.Events import Events

class Observable:
    def __init__(self):
        self.observers = {
            Events.MONITORING : [],
            Events.NEW_P : [],
            Events.DEL_P : [],
            Events.SCAN : []
        }

    def add_observer(self, observer, *events):
        for event in events:
            self.observers[event].append(observer)

    def remove_observer(self, observer, *events):
        for event in events:
            self.observers[event].remove(observer)

    def notify_observers(self, data, event):
        for obs in self.observers[event]:
            obs.update(data, event)