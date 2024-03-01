import bot.db as db
from bot.logger import Logger


def display(division_id: int):
    if division_id not in range(9):
        return "None"

    data = db.fetch("SELECT * FROM divisions WHERE id = ?", division_id)[0]

    return data[1]


def next(division_id: int):
    if division_id == 9:
        return None

    data = db.fetch("SELECT * FROM divisions WHERE id = ?", division_id + 1)[0]

    return data
