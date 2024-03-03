from bot.db import Db

class DayNightCounter:
    def __init__(self, days, nights):
        self.days = days
        self.nights = nights

    @staticmethod
    def default():
        return DayNightCounter(0, 0)

    def as_tuple(self):
        return (self.days, self.nights)

    def __repr__(self):
        return f"({self.days}|{self.nights})"

    
def display(biome_id: int):
    if biome_id > 3:
        return None

    data = Db.fetch("SELECT * FROM biomes WHERE id = ?", biome_id)[0]

    return data[1]


def ids():
    data = Db.fetch("SELECT id FROM biomes")

    # because sqlite3 always returns tuples
    return [id[0] for id in data]
