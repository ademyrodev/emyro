import bot.db as db


def display(biome_id: int):
    if biome_id > 3:
        return None

    data = db.fetch("SELECT * FROM biomes WHERE id = ?", biome_id)[0]

    return data[1]
