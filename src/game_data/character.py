from dataclasses import dataclass, field
from typing import Dict, List, Optional
from src.game_data.character_class import CharacterClass
from src.game_data.race import Race

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
    proficiencies: Dict[str, bool] = field(default_factory=dict)


# -----------------------------
# Skills
# -----------------------------
@dataclass
class Skills:
    proficiencies: Dict[str, bool] = field(default_factory=dict)


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

#-----------------------------
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
    name: str = ""
    character_class: Optional[CharacterClass] = None
    level: int = 1
    background: str = ""
    player_name: str = ""
    race: Optional[Race] = None
    alignment: str = ""
    experience_points: int = 0

    # Stats
    abilities: AbilityScores = field(default_factory=AbilityScores)
    saving_throws: SavingThrows = field(default_factory=SavingThrows)
    skills: Skills = field(default_factory=Skills)

    # Combate
    combat: CombatStats = field(default_factory=CombatStats)

    # Vida
    hp: HitPoints = field(default_factory=HitPoints)
    death_saves: DeathSaves = field(default_factory=DeathSaves)

    # Magia
    spellcasting_ability: str = ""
    spell_save_dc: int = 0
    spell_attack_bonus: int = 0

    # Otros
    inspiration: bool = False
    passive_perception: int = 10

    # Inventario
    attacks: List[Attack] = field(default_factory=list)
    proficiencies: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    equipment: List[str] = field(default_factory=list)
    features_traits: List[str] = field(default_factory=list)
    currency: Currency = field(default_factory=Currency)
    equipped_weapon = None
    equipped_armor = None

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

    def equip_armor(self, armor):
        self.equipped_armor = armor
        self.combat.armor = armor.ac
        self.calculate_armor_class()

    def equip_weapon(self, weapon):
        self.equipped_weapon = weapon
        
        attack = Attack()
        attack.name = weapon.name
        attack.damage = weapon.damage
        attack.attack_bonus = self.combat.proficiency_bonus + self.abilities.modifier("strength")
        
        self.attacks.append(attack)