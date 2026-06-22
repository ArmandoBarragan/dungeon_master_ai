import random

from src.game_engine.character import Character
from src.game_engine.quest import Quest


class Game:
    def __init__(self, game_data: dict):
        self.game_data = game_data
        self.character = self._create_random_character()
        self.quests = [self._create_quest()]

    def _create_random_character(self, **kwargs):
        data = self.game_data
        character = Character(
            name=kwargs.get("name", "Arthas"),
            character_class=random.choice(data["character_classes"]),
            level=kwargs.get("level", 1),
            race=random.choice(data["races"]),
            background=kwargs.get("background", "Soldier"),
            alignment=kwargs.get("alignment", "Lawful Good"),
            player_name=kwargs.get("player_name", "Derek"),
        )
        character.equip_weapon(random.choice(data["weapons"]))
        character.equip_armor(random.choice(data["armors"]))
        return character

    def _create_quest(self):
        return Quest()
