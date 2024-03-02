import asyncio

from datetime import datetime

from bot.logger import Logger

class World:
    daytime = False
    last_daytime_flip = -1
    day_length = 10
    day_length_seconds = 600

    @staticmethod
    async def flip_daytime():
        while True:
            World.daytime = not World.daytime
            Logger.info("Set daytime to", World.daytime)

            now = datetime.now()
            World.last_daytime_flip = now.minute

            Logger.info("Last daytime flip:", World.last_daytime_flip)

            await asyncio.sleep(World.day_length_seconds)
