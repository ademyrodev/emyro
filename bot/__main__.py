import nextcord
from nextcord.ext import commands

import bot.event as event
import bot.cmd as cmd
import bot.game.players as players

from bot.db import Db
from .config import Emyro

if __name__ == "__main__":
    intents = nextcord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(intents=intents, default_guild_ids=Emyro.guilds)

    Db.init()
    event.register_events(bot)
    cmd.register_cmds(bot)

    bot.run(Emyro.token)

    players.cleanup()
    Db.close()
