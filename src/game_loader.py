import json
from .game_data import (
    Armor,
    CharacterClass,
    Monster,
    Race,
    Weapon,
)

def load_game_into_classes(game_data):
    monster_instances = []
    for monster in monsters: # Redo for races, character classes, weapons, and armors
        monster_instances.append(Monster(
            # Load monsters into Monster class
        ))


def load_game():
    json_game_data = json.load(open("./game_data.json", 'r'))
    monsters = game_data.get("monsters")
    races = game_data.get("races")
    character_classes = game_data.get("classes")
    weapons = game_data.get("weapons")
    armors = game_data.get("armor")
    game_data = (monsters, races, character_classes, weapons, armors)
    
    game_classes = load_game_into_classes()
    if not all():
        raise Error("Game data not loaded correctly")
    return game_data
    
