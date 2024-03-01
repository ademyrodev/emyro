from bot.logger import Logger
from bot.event import Event

class OnReadyEvent(Event):
    name = "on_ready"

    async def run(self):
        Logger.info("Bot is running!")
