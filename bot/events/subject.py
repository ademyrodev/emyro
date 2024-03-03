import importlib
import os

from bot.events.events import Event
from bot.logger import Logger


class Subject:
    observers = []

    @staticmethod
    def notify(event: Event):
        for o in Subject.observers:
            o.on_notify(event)

        Logger.info("Notified event", type(event).__name__)

    @staticmethod
    def register_observers(path="bot/events/observers"):
        entries = filter(lambda e: not e.name.startswith("__"), os.scandir(path))

        for e in entries:
            full_path = os.path.join(path, e.name)

            if e.is_dir():
                Subject.register_observers(bot, full_path)
                continue

            import_path = full_path.split(".")[0]
            import_path = import_path.replace("/", ".")

            file_name = import_path.split(".")[-1]

            module = importlib.import_module(import_path)

            class_names = file_name.split("_")
            class_names = map(str.capitalize, class_names)
            class_name = "".join(class_names)
            class_ = getattr(module, class_name)

            Subject.observers.append(class_())
            Logger.info("Registered observer", class_name)
