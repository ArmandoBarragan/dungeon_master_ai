import random
from .enemy import Enemy

class Encounter:
    def __init__(self, monsters, final_encounter=False):
        self.enemies = []
        if final_encounter:
            bosses = monsters.filtered(lambda x: x.behavior == "Jefe")
            self.enemies.append(Enemy(random.choice(bosses)))
        else:
            pack = random.randint(0, 1)
            if pack:
                mid_sized_species = monsters.filtered(lambda x: x.behavior == "Solitario")
                species = random.choice(mid_sized_species)
                enemies = [Enemy(species) for i in range(0, 2)]
            else:
                small_species = monsters.filtered(lambda x: x.behavior == "Manada")
                species = random.choice(small_species)
                enemies = [Enemy(species)]

        