import random
from typing import Any

from .attack import Attack
from .item import Item
from .monster_species import MonsterSpecies

class Enemy:
    name: str
    species: MonsterSpecies
    gold_loot: int
    items_loot: list[Item]
    reward_experience: int
    hp: int
    constitution: int
    dexterity: int

    def __init__(self, enemy_data: dict[str, Any]):
        self.name = enemy_data.get("name")
        self.species = MonsterSpecies(enemy_data.get("species"))
        reward = enemy_data.get("reward") or {}
        loot = reward.get("loot") or {}
        self.gold_loot = loot.get("gold", 0)
        self.items_loot = [Item(item) for item in loot.get("items", [])]
        self.reward_experience = reward.get("experience", 0)
        self._calculate_attributes()

        attacks = enemy_data.get("attacks") or self.species.attacks
        self.attacks = [Attack(attack) for attack in attacks]

    def _calculate_attributes(self):
        if self.species.size == "Small":
            self.hp = sum([random.randint(1, 6), random.randint(1, 6)])
            self.constitution = 10 + random.randint(0, 2)
            self.dexterity = random.randint(3, 6) + random.randint(1, 3)
        elif self.species.size == "Medium":
            self.hp = sum([random.randint(1, 6) for i in range(6)])
            self.constitution = 10 + random.randint(3, 5)
            self.dexterity = random.randint(1, 4) + random.randint(1, 3)
        else:
            self.hp = sum([random.randint(1, 6) for i in range(15)])
            self.constitution = random.randint(6, 8)
            self.dexterity = random.randint(1, 4) + random.randint(1, 3)
        