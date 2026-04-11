import json
import random
class Monster:
    def __init__(self, name, size, behavior, attacks):
        self.name = name
        self.size = size
        self.behavior = behavior
        self.attacks = attacks

    def to_dict(self):
        return {
            "name": self.name,
            "size": self.size,
            "behavior": self.behavior,
            "attacks": self.attacks,
        }
    
    @classmethod
    def random_monster(cls, path="quest.json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        monster_data = random.choice(data["monsters"])

        return cls(
            name=monster_data["name"],
            size=monster_data["size"],
            behavior=monster_data["behavior"],
            attacks=monster_data["attacks"],
        )