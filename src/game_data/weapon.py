import json
import random

class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

    def to_dict(self):
        return {
            "name": self.name,
            "damage": self.damage,
        }
    
    @classmethod
    def random_weapon(cls, path="quest.json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        weapon_data = random.choice(data["weapons"])

        return cls(
            name=weapon_data["name"],
            damage=weapon_data["damage"],
        )