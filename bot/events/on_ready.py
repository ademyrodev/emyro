import asyncio

from bot.logger import Logger
from bot.event import Event

class OnReadyEvent(Event):
    name = "on_ready"

    async def run(self):
        Logger.info("Emyro's ready!")

        asyncio.create_task(self.time_timer())

    async def time_timer(self):
        while True:
            Logger.info("Timer task executed!")
            await asyncio.sleep(10)

            # temporary placeholder.
            ...
