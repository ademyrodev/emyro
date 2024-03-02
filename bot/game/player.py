from bot.game.biomes import DayNightCounter

class Player:
    def __init__(
        self,
        id: int,
        level: int,
        xp: int,
        req_xp: int,
        hp: int,
        energy: int,
        coins: int,
        division: int,
        biome: int,
        biomes: list[DayNightCounter]
    ):

        self.id = id
        self.level = level
        self.xp = xp
        self.req_xp = req_xp
        self.hp = hp
        self.energy = energy
        self.coins = coins
        self.division = division
        self.biome = biome
        self.biomes = biomes

    @staticmethod
    def default(id):
        day_night = DayNightCounter.default() 

        return Player(id, 1, 0, 25, 100, 50, 0, 0, 0, day_night)

    @staticmethod
    def from_raw(tuple_data):
        return Player(*tuple_data)
