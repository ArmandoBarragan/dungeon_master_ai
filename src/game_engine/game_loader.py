import json
from pathlib import Path

from .game_data import (
    Armor,
    CharacterClass,
    Monster,
    Race,
    Weapon,
)

def load_game_into_classes(game_data):
    monster_instances = []
    for monster in game_data.get("monsters", []):
        if isinstance(monster, Monster):
            monster_instances.append(monster)
            continue
         # Redo for races, character classes, weapons, and armors
        monster_instances.append(Monster(
            # Load monsters into Monster class
            name=monster.get("name"),
            size=monster.get("size"),
            behavior=monster.get("behavior"),
            attacks=monster.get("attacks"),
        ))

    armor_instances = []
    for armor in game_data.get("armors", []):
        if isinstance(armor, Armor):
            armor_instances.append(armor)
            continue
        armor_instances.append(Armor(
            name=armor.get("name"),
            ac=armor.get("ac"),
        ))

    character_classes_instances = []
    for character_class in game_data.get("character_classes", []):
        if isinstance(character_class, CharacterClass):
            character_classes_instances.append(character_class)
            continue
        character_classes_instances.append(CharacterClass(
            name=character_class.get("name"),
            hit_die=character_class.get("hit_die"),
            features=character_class.get("features"),
            proficiencies=character_class.get("proficiencies"),
        ))

    race_instances = []
    for race in game_data.get("races", []):
        if isinstance(race, Race):
            race_instances.append(race)
            continue
        race_instances.append(Race(
            name=race.get("name"),
            attributes=race.get("attributes"),
            features=race.get("features"),
        ))
    
    weapon_instances = []
    for weapon in game_data.get("weapons", []):
        if isinstance(weapon, Weapon):
            weapon_instances.append(weapon)
            continue
        weapon_instances.append(Weapon(
            name=weapon.get("name"),
            damage=weapon.get("damage"),
        ))
    return {
        "monsters": monster_instances,
        "armors": armor_instances,
        "races": race_instances,
        "weapons": weapon_instances,
        "character_classes": character_classes_instances,
    }


def load_game():
    game_data_path = Path(__file__).resolve().parent / "game_data" / "game_data.json"
    with open(game_data_path, encoding="utf-8") as f:
        raw = json.load(f)

    monsters = raw.get("monsters")
    races = raw.get("races")
    character_classes = raw.get("classes")
    weapons = raw.get("weapons")
    armors = raw.get("armors")
    game_data = {
        "monsters": monsters,
        "races": races,
        "character_classes": character_classes,
        "weapons": weapons,
        "armors": armors,
    }

    if not all([monsters, races, character_classes, weapons, armors]):
        raise RuntimeError("Game data not loaded correctly")
    return load_game_into_classes(game_data)
