import random
from .encounter import Encounter


def generate_random_location() -> str:
    """Devuelve un nombre de lugar de fantasía construido a partir de partes seleccionadas."""
    prefixes = (
        "Roca del Castillo",
        "Whiskey",
        "Bosque Profundo",
        "Ocaso",
        "Pico de Hierro",
        "Valle Brumoso",
        "Pino de Plata",
        "Piedra Vieja",
        "Descanso del Cuervo",
        "Lago de Escarcha",
        "Espina de Espino",
        "Vado de Ceniza",
        "Ascua",
        "Luz de Luna",
    )
    sufixes = (
        "del Valle",
        "de la Aldea",
        "del Sendero",
        "de los Bosques",
        "del Cruce",
        "del Hueco",
        "de la Cresta",
        "de la Marisma",
        "del Torreón",
        "del Claros",
        "de las Cataratas",
        "del Brezal",
    )
    return f"{random.choice(prefixes)} {random.choice(sufixes)}"


class Quest:
    def __init__(self, monsters):
        self.reward = random.randint(400, 800)
        self.location = generate_random_location()
        self._generate_encounters(monsters)

    def _generate_encounters(self, monsters):
        self.encounters = []
        self.encounters.append(Encounter(monsters))
        self.encounters.append(Encounter(monsters))
        final_encounter = Encounter(monsters, True)
        self.boss = final_encounter.enemies[0].species.name
        self.encounters.append(final_encounter)

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "reward": self.reward,
            "boss": self.boss,
            "location": self.location,
        }
    