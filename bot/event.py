import importlib
import os
from abc import ABC, abstractmethod

import nextcord
from nextcord.ext import commands

from bot.logger import Logger

class Event(ABC):
    name = None

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        if not self.name:
            raise ValueError("No event name provided.")

        if not self.name.startswith("on_"):
            raise NameError("Invalid event name.")

        self.register_event()
        
    def register_event(self):
        event_fun = self.bot.listen(self.name)(self.run)

        setattr(self, "run", event_fun)

        Logger.info("Registered event", self.name)

    @abstractmethod 
    async def run(self):
        raise NotImplementedError(f"Event {self.name} not implemented.")

def register_events(bot: commands.Bot, path="bot/events"):
    entries = filter(lambda e: not e.name.startswith("__"), os.scandir(path))

    for e in entries:
        full_path = os.path.join(path, e.name)
        
        if e.is_dir():
            register_cmds(bot, full_path)
            continue

        import_path = full_path.split(".")[0]
        import_path = import_path.replace("/", ".")

        file_name = import_path.split(".")[-1]

        module = importlib.import_module(import_path)

        class_names = file_name.split("_")
        class_names = map(str.capitalize, class_names)
        class_name = "".join(class_names)
        class_name = getattr(module, f"{class_name}Event")

        class_name(bot)
