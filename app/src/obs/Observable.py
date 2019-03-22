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
        self.print_stats()

    def add_observer(self, observer, *events):
        for event in events:
            self.observers[event].append(observer)
        self.print_stats()

    def remove_observer(self, observer, *events):
        for event in events:
            self.observers[event].remove(observer)
        self.print_stats()

    def notify_observers(self, data, event):
        for obs in self.observers[event]:
            obs.update(data, event)

    def print_stats(self):
        print('------OBSERVABLE STATS---------')
        print(len(self.observers[1]))
        print(len(self.observers[2]))
        print(len(self.observers[3]))
        print(len(self.observers[4]))
        print('--------------------------------')