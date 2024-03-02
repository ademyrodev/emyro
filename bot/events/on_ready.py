import asyncio

from datetime import datetime

from bot.game.world import World

from bot.logger import Logger
from bot.event import Event

class OnReadyEvent(Event):
    name = "on_ready"

    async def run(self):
        Logger.info("Emyro's ready!")

        asyncio.create_task(World.flip_daytime())
