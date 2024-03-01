import importlib
import os
from abc import ABC, abstractmethod

import nextcord
from nextcord.ext import commands

from .config import Emyro
from .logger import Logger


class Cmd(ABC):
    name: str = None
    desc: str = None

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        if not self.name:
            raise ValueError("Missing command name.")

        if not self.desc:
            raise ValueError("Missing description.")

        self.register_cmd()

    def register_cmd(self):
        # decorator workaround
        cmd_fun = self.bot.slash_command(
            name=self.name, description=self.desc, guild_ids=Emyro.guilds
        )(self.run)

        setattr(self, "run", cmd_fun)

        Logger.info("Registered command", self.name)

    @abstractmethod
    async def run(self, interaction: nextcord.Interaction):
        raise NotImplementedError(f"Command {self.name} not implemented.")


def register_cmds(bot: commands.Bot, path="bot/cmds"):
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
        class_name = getattr(module, f"{file_name.capitalize()}Cmd")

        class_name(bot)
