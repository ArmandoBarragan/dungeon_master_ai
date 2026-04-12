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
