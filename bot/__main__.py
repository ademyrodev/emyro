import asyncio

import nextcord
from nextcord.ext import commands

import bot.cmd as cmd
import bot.game.players as players
from bot.events.subject import Subject
from bot.game.world import World

from .config import Emyro
from .db import Db
from .logger import Logger

if __name__ == "__main__":
    intents = nextcord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(intents=intents, default_guild_ids=Emyro.guilds)

    Db.init()
    Subject.register_observers()
    cmd.register_cmds(bot)

    @bot.event
    async def on_ready():
        Logger.info("Emyro's ready!")

        Logger.info("Creating timer task...")
        asyncio.create_task(World.flip_daytime())

    bot.run(Emyro.token)

    players.cleanup()
    Db.close()
