import json
from bot.game.nature import Nature
from bot.game.spell import Spell

class Equipment:
    def __init__(
        self, 
        name: str,
        nature: Nature,
        enhancements: list[Spell],
        speed: int,
        attack: int,
        defense: int
    ):
        self.name = name
        self.nature = nature
        self.enhancements = enhancements
        self.speed = speed
        self.attack = attack
        self.defense = defense

    @staticmethod
    def none():
        return Equipment(
            "None",
            Nature.NONE,
            [],
            0,
            0,
            0
        )

    @staticmethod
    def from_json(player_json: str):
        as_dict = json.loads(player_json) 

        name = as_dict["name"]
        nature = Nature(as_dict["nature"])
        enhancements = Spell.get_enhancements(as_dict["enhancements"])

        speed = as_dict["speed"]
        attack = as_dict["attack"]
        defense = as_dict["defense"]

        item = Equipment(name, nature, enhancements, speed, attack, defense)

        return item
    
    def json(self):
        as_dict = {
            "name": self.name,
            "nature": self.nature,
            "enhancements": [e.as_dict() for e in self.enhancements],
            "speed": self.speed, 
            "attack": self.attack,
            "defense": self.defense
        }
        
        return json.dumps(as_dict)
    
