from abc import ABC, abstractmethod

from bot.events.events import Event

class Observer(ABC):
    def __init__(self):
        ... 
        
    @abstractmethod 
    def on_notify(self, event: Event):
        raise NotImplementedError(f"Observer {self.name} not implemented.")


