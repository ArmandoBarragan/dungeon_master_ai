import json
import random

class Race:
    def __init__(self, name, attributes, features):
        self.name = name
        self.attributes = attributes
        self.features = features

    def to_dict(self):
        return {
            "name": self.name,
            "attributes": self.attributes,
            "features": self.features,
        }
    
    @classmethod
    def random_race(cls, path="quest.json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        race_data = random.choice(data["races"])

        return cls(
            name=race_data["name"],
            attributes=race_data["attributes"],
            features=race_data["features"],
        )