import json
from enum import Enum

from bot.game.spell import Spell


class Consumable:
    def __init__(
        self,
        name: str,
        spell: Spell,
        is_harmful: bool,
        contains_seed: bool,
        amount: int,
    ):
        self.name = name
        self.spell = spell
        self.is_harmful = is_harmful
        self.contains_seed = contains_seed
        self.amount = amount

    @staticmethod
    def none():
        return Consumable("None", None, False, False, 0)

    @staticmethod
    def from_json(as_dict: dict):
        name = as_dict["name"]
        spell = Spell.from_json(as_dict["spell"])
        is_harmful = as_dict["is_harmful"]
        contains_seed = as_dict["contains_seed"]
        amount = as_dict["amount"]

        return Consumable(name, spell, is_harmful, contains_seed, amount)

    def as_dict(self):
        as_dict = {
            "name": self.name,
            "spell": self.spell.as_dict(),
            "is_harmful": self.is_harmful,
            "contains_seed": self.contains_seed,
            "amount": self.amount,
        }

        return as_dict


class Inventory:
    def __init__(self, items: list[Consumable]):
        self.items = items

    @staticmethod
    def empty():
        return Inventory([])

    @staticmethod
    def from_json(inventory_json: str):
        as_dict = json.loads(inventory_json)

        as_list = [Consumable.from_json(e) for e in as_dict]

        return Inventory(as_list)

    def add(self, item: Consumable):
        if self.is_full():
            raise FullInventoryError()

        self.items.append(item)

    def is_full(self):
        return len(self.items) == 8

    def is_empty(self):
        return len(self.items) == 0

    def json(self):
        as_list = [c.as_dict() for c in self.items]

        return json.dumps(as_list)

    def __getitem__(self, index):
        return self.items[index]


class FullInventoryError(Exception): ...
