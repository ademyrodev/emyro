import bot.db as db


class DayNightCounter:
    def __init__(self, days, nights):
        self.days = days
        self.nights = nights

    @staticmethod
    def default():
        return DayNightCounter(0, 0)

    
def display(biome_id: int):
    if biome_id > 3:
        return None

    data = db.fetch("SELECT * FROM biomes WHERE id = ?", biome_id)[0]

    return data[1]
