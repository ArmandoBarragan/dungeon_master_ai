import json
import random

class CharacterClass:
    def __init__(self, name, hit_die, features, proficiencies):
        self.name = name
        self.hit_die = hit_die
        self.features = features
        self.proficiencies = proficiencies

    def to_dict(self):
        return {
            "name": self.name,
            "hit_die": self.hit_die,
            "features": self.features,
            "proficiencies": self.proficiencies,
        }
