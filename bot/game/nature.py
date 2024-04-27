from enum import Enum


class Nature(Enum):
    NONE = 0
    FIRE = 1
    AIR = 2
    WATER = 3
    EARTH = 4
    LIGHT = 5
    DARK = 6
    FROST = 7
    SAND = 8
    DECAY = 9

    def defeats(self, other):
        return other in ADVANTAGES[self.value]

    def __plus__(self, other):
        if self.value == other.value:
            return self

        left = Nature(min(self.value, other.value))
        right = Nature(max(self.value, other.value))

        return COMBINATIONS[left][right]


ADVANTAGES = {
    Nature.FIRE: [Nature.AIR, Nature.EARTH, Nature.FROST],
    Nature.AIR: [Nature.EARTH, Nature.SAND, Nature.DECAY],
    Nature.WATER: [Nature.FIRE, Nature.AIR, Nature.DECAY],
    Nature.FROST: [Nature.AIR, Nature.WATER, Nature.SAND],
    Nature.SAND: [Nature.FIRE, Nature.WATER, Nature.DECAY],
    Nature.DECAY: [Nature.FIRE, Nature.EARTH, Nature.FROST],
}

COMBINATIONS = {
    Nature.NONE: [
        Nature.FIRE,
        Nature.AIR,
        Nature.WATER,
        Nature.EARTH,
        Nature.FROST,
        Nature.SAND,
        Nature.DECAY,
    ],
    Nature.FIRE: [
        Nature.FIRE,
        Nature.FIRE,
        Nature.AIR,
        Nature.SAND,
        Nature.WATER,
        Nature.EARTH,
        Nature.DECAY,
    ],
    Nature.AIR: [
        Nature.AIR,
        Nature.FROST,
        Nature.DECAY,
        Nature.WATER,
        Nature.SAND,
        Nature.DECAY,
    ],
    Nature.WATER: [
        Nature.WATER,
        Nature.EARTH,
        Nature.FROST,
        Nature.DECAY,
        Nature.EARTH,
    ],
    Nature.EARTH: [Nature.EARTH, Nature.WATER, Nature.AIR, Nature.SAND],
    Nature.FROST: [Nature.FROST, Nature.EARTH, Nature.WATER],
    Nature.SAND: [Nature.SAND, Nature.FIRE],
    Nature.DECAY: [Nature.DECAY],
}
