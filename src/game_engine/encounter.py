import random
from .enemy import Enemy

class Encounter:
    def __init__(self, monsters, final_encounter=False):
        self.enemies = []
        
        if final_encounter:
            # Usamos list comprehension para filtrar
            bosses = [m for m in monsters if m.behavior == "Jefe"]
            if bosses:
                self.enemies.append(Enemy(random.choice(bosses)))
        else:
            pack = random.randint(0, 1)
            if pack:
                # Filtrar monstruos solitarios
                mid_sized = [m for m in monsters if m.behavior == "Solitario"]
                if mid_sized:
                    species = random.choice(mid_sized)
                    # Creamos la lista de enemigos (2 en este caso)
                    self.enemies = [Enemy(species) for _ in range(2)]
            else:
                # Filtrar monstruos de manada
                small_species = [m for m in monsters if m.behavior == "Manada"]
                if small_species:
                    species = random.choice(small_species)
                    self.enemies = [Enemy(species)]