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
    