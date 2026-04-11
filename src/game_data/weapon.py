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
