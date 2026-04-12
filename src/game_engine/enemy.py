import random 


class Enemy:
    def __init__(self, species):
        self.species = species
        self._calculate_attributes()

    def _calculate_attributes():
        if self.species.size == "Pequeño":
            self.hp = sum([random.randint(1, 6), random.randint(1, 6)])
            self.constituion = 10 + random.randint(0, 2)
            self.dexterity = random.randint(3, 6) + random.randint(1, 3)
            self.loot = random.randint(0, 15)
        elif self.species.size == "Mediano":
            self.hp = sum([random.randint(1, 6) for i in range(6)])
            self.constituion = 10 + random.randint(3, 5)
            self.dexterity = random.randint(1, 4) + random.randint(1, 3)
            self.loot = random.randint(0, 20)
        else:
            self.hp = sum([random.randint(1, 6) for i in range(15)])
            self.constituion = random.randint(6, 8)
            self.dexterity = random.randint(1, 4) + random.randint(1, 3)
            self.loot = random.randint(200, 500)
        