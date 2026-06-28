from .armor import Armor
from .character_class import CharacterClass
from .race import Race
from .weapon import Weapon


class Character:
    def __init__(
        self,
        name: str,
        character_class: CharacterClass,
        level: int,
        race: Race,
        background: str,
        alignment: str,
        player_name: str,
    ):
        self.name = name
        self.character_class = character_class
        self.level = level
        self.race = race
        self.background = background
        self.alignment = alignment
        self.player_name = player_name
        self.weapon: Weapon | None = None
        self.armor: Armor | None = None
        self.hp = 0
        self.constitution = 10
        self.dexterity = 10
        self.strength = 10
        self.wisdom = 10
        self.intelligence = 10
        self.charisma = 10
        self._apply_race_attributes()

    def _apply_race_attributes(self):
        pass

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon

    def equip_armor(self, armor: Armor):
        self.armor = armor

    def to_dict(self):
        return {
            "name": self.name,
            "character_class": self.character_class.to_dict(),
            "level": self.level,
            "race": self.race.to_dict(),
            "background": self.background,
            "alignment": self.alignment,
            "player_name": self.player_name,
            "weapon": self.weapon.to_dict() if self.weapon else None,
            "armor": self.armor.to_dict() if self.armor else None,
        }
