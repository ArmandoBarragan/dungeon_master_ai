import json
import random

class Armor:
    def __init__(self, name, ac):
        self.name = name
        self.ac = ac

    def to_dict(self):
        return {
            "name": self.name,
            "ac": self.ac,
        }
    
    @classmethod
    def random_armor(cls, path="quest.json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        armor_data = random.choice(data["armor"])

        return cls(
            name=armor_data["name"],
            ac=armor_data["ac"],
        )
    
