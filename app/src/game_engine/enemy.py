import random 
from typing import Any
from .game_data.monster import Monster

class Enemy:
    species: str
    loot: int
    reward_experience: int
    hp: int
    constitution: int
    dexterity: int

    def __init__(self, enemy_data: dict[str, Any]):
        self.species = enemy_data.get("species")
        self.loot = enemy_data.get("loot")
        self.reward_experience = enemy_data.get("reward_experience")
        self._calculate_attributes()
        attacks = enemy_data.get("attacks")
        self.attacks = [Attack(attack) for attack in attacks]

    def _calculate_attributes(self):
        if self.species.get("size") == "Small":
            self.hp = sum([random.randint(1, 6), random.randint(1, 6)])
            self.constitution = 10 + random.randint(0, 2)
            self.dexterity = random.randint(3, 6) + random.randint(1, 3)
        elif self.species.get("size") == "Medium":
            self.hp = sum([random.randint(1, 6) for i in range(6)])
            self.constitution = 10 + random.randint(3, 5)
            self.dexterity = random.randint(1, 4) + random.randint(1, 3)
        else:
            self.hp = sum([random.randint(1, 6) for i in range(15)])
            self.constitution = random.randint(6, 8)
            self.dexterity = random.randint(1, 4) + random.randint(1, 3)
        