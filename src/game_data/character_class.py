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
    
    @classmethod
    def random_class(cls, path="quest.json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        class_data = random.choice(data["classes"])

        return cls(
            name=class_data["name"],
            hit_die=class_data["hit_die"],
            features=class_data["features"],
            proficiencies=class_data["proficiencies"],
        )

