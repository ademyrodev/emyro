from enum import Enum
from typing import Optional

import json

from bot.game.nature import Nature
from bot.util import roman
from bot.logger import Logger


class Intent(Enum):
    DAMAGE = 0
    HEAL = 1

    def __repr__(self):
        return self.name.capitalize()


class Intensity(Enum):
    PASSIVE = 0
    LOW = 1
    MID = 2
    EFFECTIVE = 3
    HIGH = 4
    POWERFUL = 5
    NOTEWORTHY = 6
    REMARKABLE = 7
    IMPRESSIVE = 8
    MIGHTY = 9
    OMNIPOTENT = 10

    def cost(self):
        return self.value * 15

    def __repr__(self):
        return roman.roman(self.value)


class Effect(Enum):
    WEAKNESS = 0
    STRENGTH = 1
    SLOWNESS = 2
    SPEED = 3
    CONFUSION = 4
    FOCUS = 5

    def __repr__(self):
        return self.name.capitalize()


class Status:
    def __init__(self, effect: Effect, intensity: Intensity, turns: int):
        self.effect = effect
        self.intensity = intensity
        self.turns = turns

    def as_dict(self):
        as_dict = {
            "effect": self.effect.value,
            "intensity": self.intensity.value,
            "turns": self.turns,
        }

        return as_dict

    @staticmethod
    def from_dict(as_dict: dict):
        effect = Effect(as_dict["effect"])
        intensity = Intensity(as_dict["intensity"])
        turns = as_dict["turns"]

        return Status(effect, intensity, turns)

    def __repr__(self):
        return f"{self.effect} {self.intensity} ({self.turns} turns)"


class Spell:
    def __init__(
        self,
        name: str,
        nature: Nature,
        intent: Intent,
        intensity: Intensity,
        side_effect: Optional[Status] = None,
    ):
        self.name = name
        self.nature = nature
        self.intent = intent
        self.intensity = intensity
        self.side_effect = side_effect

    @staticmethod
    def default():
        default_spell = Spell(
            ":wind_blowing_face: Wind Gust",
            Nature.AIR,
            Intent.DAMAGE,
            Intensity.LOW,
            None
        )

        return default_spell

    def as_dict(self):
        Logger.info("Saving spell", self, "with intent", self.intent, "and side effect of", self.side_effect)

        as_dict = {
            "name": self.name,
            "nature": self.nature.value,
            "intent": self.intent.value,
            "intensity": self.intensity.value,
            "side_effect": self.side_effect.as_dict() if self.side_effect is not None else None,
        }

        return as_dict

    @staticmethod
    def from_dict(as_dict: dict):
        name = as_dict["name"]
        nature = Nature(as_dict["nature"])
        intent = Intent(as_dict["intent"])
        intensity = Intensity(as_dict["intensity"])

        side_effect = (
            Status.from_dict(as_dict["side_effect"])
            if as_dict["side_effect"] is not None
            else None
        )

        return Spell(name, nature, intent, intensity, side_effect)

    @staticmethod
    def get_enhancements(enhancements: list):
        enhancements = [Spell.from_dict(e) for e in enhancements]

        return enhancements

    def __repr__(self):
        return f"{self.name} {self.intensity.__repr__()}"

class SpellBook:
    def __init__(self, spells: list[Spell]):
        self.spells = spells

    @staticmethod
    def default():

        return SpellBook([Spell.default()])

    @staticmethod
    def from_json(book_json: str):
        as_list = json.loads(book_json)
        spells = [Spell.from_dict(s) for s in as_list]

        return SpellBook(spells)
        
    def add(self, spell: Spell):
        if self.is_full():
            raise FullSpellbookError()

        self.spells.append(spell)

    def is_full(self):
        return len(self.spells) == 4

    def count(self):
        return len(self.spells)

    def json(self):
        as_list = [s.as_dict() for s in self.spells]

        return json.dumps(as_list)

    def __getitem__(self, index: int):
        return self.spells[index]

class FullSpellbookError(Exception): ...