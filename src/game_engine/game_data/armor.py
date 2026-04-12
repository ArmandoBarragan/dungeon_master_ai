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

    
