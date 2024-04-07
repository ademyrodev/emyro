from enum import Enum
from typing import Optional

from bot.game.nature import Nature

class Intent(Enum):
    DAMAGE = 0
    HEAL = 1

class Intensity(Enum):
    LOW = 0
    MID = 1
    HIGH = 2

    def __repr__(self):
        return "I" * (self.value + 1)

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
    def __init__(
        self, 
        effect: Effect, 
        intensity: Intensity,
        turns: int
    ):
        self.effect = effect
        self.intensity = intensity
        self.turns = turns

    def as_dict(self):
        as_dict = {
            "effect": self.effect.value,
            "intensity": self.intensity.value,
            "turns": self.turns
        }

        return as_dict

    def from_json(self, as_dict: dict):
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
        side_effect: Optional[Status] = None
    ):
        self.name = name
        self.nature = nature
        self.intent = intent
        self.intensity = intensity
        self.side_effect = side_effect

    def as_dict(self):
        as_dict = {
            "name": self.name,
            "intent": self.intent.value,
            "intensity": self.intensity.value,
            "side_effect": self.status.as_dict()            
        }

        return as_dict

    def from_json(self, as_dict: dict):
        name = as_dict["name"]  
        intent = Intent(as_dict["intent"])
        intensity = Intensity(as_dict["intensity"])

        side_effect = Status.from_json(as_dict["side_effect"])

        return Spell(name, intent, intensity, side_effect)

    @staticmethod
    def get_enhancements(enhancements: list):
        enhancements = [Spell.from_json(e) for e in enhancements]

        return enhancements

    def __repr__(self):
        return f"{self.name} {self.intensity}"
                 

