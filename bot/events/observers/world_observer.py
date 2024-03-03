import bot.events.events as events
import bot.game.players as players

from bot.game.biomes import DayNightCounter
from bot.game.world import World
from bot.events.observer import Observer

class WorldObserver(Observer):
    def on_notify(self, event: events.Event):
        if isinstance(event, events.DaytimeFlipEvent):
            self.increment_player_day_count()

    def increment_player_day_count(self):
        # maybe not the most fair solution?
        active_cache = players.player_cache.values()

        for c in active_cache:
            player = c.player
            self.increment_day_count(player.total_days)

            if c.has_changed_biome:
                continue

            biome = player.biome
            self.increment_day_count(player.biomes[biome])
    
    def increment_day_count(
        self, 
        counter: DayNightCounter 
    ):
        if not World.daytime:
            counter.days += 1
        else:
            counter.nights += 1
            
