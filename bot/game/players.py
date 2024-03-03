import nextcord

from bot.db import Db
from bot.game.player import Player
from bot.logger import Logger

CACHE_LIMIT = 55
player_cache = {}


class CachedPlayer:
    def __init__(self, player: Player):
        self.player = player
        self.uses = 0
        self.has_changed_biome = False

    def increment_uses(self):
        self.uses += 1


def expel(cached: CachedPlayer):
    player = cached.player

    player.update()

    Logger.info("Expelled from the cache and saved player with ID", player.id)


def filter_out_unused_cache():
    evicted_amount = CACHE_LIMIT * 0.20

    least_used_cache = sorted(player_cache.values(), key=lambda p: p.uses)
    evicted_cache = least_used_cache[:evicted_amount]

    for e in evicted_cache:
        expel(e)
        del player_cache[e.player.id]


def cache(player: Player):
    cached = CachedPlayer(player)

    if len(player_cache) >= CACHE_LIMIT:
        filter_out_unused_cache()

    player_cache[cached.player.id] = cached

    Logger.info("Cached player with ID", player.id)


def find_from_db(player_id: int):
    player = Player.fetch_from_db(player_id)

    cache(player)
    return player


def find(player_id: int):
    try:
        cached = player_cache[player_id]
        cached.increment_uses()

        return cached.player
    except KeyError:
        return find_from_db(player_id)


def cleanup():
    Logger.info("Cleaning up cache...")

    cache_copy = dict(player_cache)

    for k, v in cache_copy.items():
        expel(v)
        del player_cache[k]
