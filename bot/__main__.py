import nextcord
from nextcord.ext import commands

import bot.cmd as cmd
import bot.db as db
import bot.game.players as players

from .config import Emyro

if __name__ == "__main__":
    intents = nextcord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(intents=intents, default_guild_ids=Emyro.guilds)

    db.init()
    cmd.register_cmds(bot)

    bot.run(Emyro.token)

    players.cleanup()
    db.close()
