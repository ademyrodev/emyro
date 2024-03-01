import asyncio

from datetime import datetime

from bot.game.world import World

from bot.logger import Logger
from bot.event import Event

class OnReadyEvent(Event):
    name = "on_ready"

    async def run(self):
        Logger.info("Emyro's ready!")

        asyncio.create_task(self.time_timer())

    async def time_timer(self):
        while True:
            World.daytime = not World.daytime
            Logger.info("Set daytime to", World.daytime)

            now = datetime.now()
            World.last_daytime_flip = (now.minute, now.second)

            Logger.info("Last daytime flip:", World.last_daytime_flip)

            await asyncio.sleep(30)
            # temporary placeholder.
            ...
