import random
import json
from pathlib import Path

from src.game_engine.character import Character
from src.game_engine.quest import Quest

GAME_DATA_PATH = Path(__file__).resolve().parent / "game_engine" / "game_data.json"


class Game:
    def __init__(self):
        self.character = self._create_random_character()
        self.quests = [self._create_quest()]

    def _load_game_data(self) -> dict:
        with open(GAME_DATA_PATH, encoding="utf-8") as f:
            game_data = json.load(f)
        return game_data

    def _create_random_character(self, **kwargs):
        data = self._load_game_data()
        character_classes = list(data["character_classes"].keys())
        races = list(data["races"].keys())
        weapons = list(data["weapons"].keys())
        armors = list(data["armors"].keys())
        character = Character(
            name=kwargs.get("name", "Arthas"),
            character_class=random.choice(character_classes),
            level=kwargs.get("level", 1),
            race=random.choice(races),
            background=kwargs.get("background", "Soldier"),
            alignment=kwargs.get("alignment", "Lawful Good"),
            player_name=kwargs.get("player_name", "Derek"),
        )
        character.equip_weapon(random.choice(weapons))
        character.equip_armor(random.choice(armors))
        return character

    def _create_quest(self):
        return Quest(story_key="monster_in_town")
