from dataclasses import dataclass, field


# -----------------------------
# Atributos base
# -----------------------------
@dataclass
class AbilityScores:
    strength = 10
    dexterity = 10
    constitution = 10
    intelligence = 10
    wisdom = 10
    charisma = 10

    def modifier(self, stat):
        value = getattr(self, stat)
        return (value - 10) // 2


# -----------------------------
# Saving Throws
# -----------------------------
@dataclass
class SavingThrows:
    proficiencies = field(default_factory=dict)


# -----------------------------
# Skills
# -----------------------------
@dataclass
class Skills:
    proficiencies = field(default_factory=dict)


# -----------------------------
# Combate
# -----------------------------
@dataclass
class CombatStats:
    def __init__(self):
        self.base_ac = 10
        self.armor = 0
        self.shield = 0
        self.initiative = 0
        self.speed = 30
        self.proficiency_bonus = 2
        self.armor_class = 10


# -----------------------------
# HP
# -----------------------------
@dataclass
class HitPoints:
    max_hp = 0
    current_hp = 0
    temp_hp = 0


# -----------------------------
# Death Saves
# -----------------------------
@dataclass
class DeathSaves:
    successes = 0
    failures = 0


# -----------------------------
# Ataques
# -----------------------------
@dataclass
class Attack:
    name = ""
    attack_bonus = 0
    damage = ""
    range = ""


# -----------------------------
# Monedas
# -----------------------------
@dataclass
class Currency:
    cp = 0
    sp = 0
    ep = 0
    gp = 0
    pp = 0


# -----------------------------
# Personaje principal
# -----------------------------
@dataclass
class Character:
    # Info básica
    name = ""
    character_class = ""
    level = 1
    background = ""
    player_name = ""
    race = ""
    alignment = ""
    experience_points = 0

    # Stats
    abilities = field(default_factory=AbilityScores)
    saving_throws = field(default_factory=SavingThrows)
    skills = field(default_factory=Skills)

    # Combate
    combat = field(default_factory=CombatStats)

    # Vida
    hp = field(default_factory=HitPoints)
    death_saves = field(default_factory=DeathSaves)

    # Magia
    spellcasting_ability = ""
    spell_save_dc = 0
    spell_attack_bonus = 0

    # Otros
    inspiration = False
    passive_perception = 10

    # Inventario
    attacks = field(default_factory=list)
    proficiencies = field(default_factory=list)
    languages = field(default_factory=list)
    equipment = field(default_factory=list)
    features_traits = field(default_factory=list)
    currency = field(default_factory=Currency)

    # -------------------------
    # Métodos útiles
    # -------------------------
    def calculate_initiative(self):
        self.combat.initiative = self.abilities.modifier("dexterity")

    def calculate_passive_perception(self):
        self.passive_perception = 10 + self.abilities.modifier("wisdom")

    def add_attack(self, attack):
        self.attacks.append(attack)

    def calculate_armor_class(self):
        dex_mod = self.abilities.modifier("dexterity")
        
        self.combat.armor_class = (
            self.combat.base_ac +
            dex_mod +
            self.combat.armor +
            self.combat.shield
        )