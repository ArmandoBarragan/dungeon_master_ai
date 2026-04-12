import random

from src.game_engine.character import Character
from src.game_engine.game_loader import load_game
from src.game_engine.quest import Quest


class Game:
    def __init__(self, game_data=None):
        self.game_data = game_data or load_game()
        self.character = None
        self.quests = []
        self.current_encounter_index = 0

    @classmethod
    def create_new(cls, game_data=None, **character_kwargs):
        game = cls(game_data)
        game.character = game._create_random_character(**character_kwargs)
        game.quests.append(game._create_quest())
        return game

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

    def start_quest(self):
        # 1. Generate first encounter
        # 2. Generate second encounter
        # 3. Generate boss encounter
        pass

    def to_dict(self):
        return {
            "character": self.character.to_dict() if self.character else None,
            "quests": [self._quest_to_dict(quest) for quest in self.quests],
            "current_encounter_index": self.current_encounter_index,
        }

    def _quest_to_dict(self, quest):
        return {
            "initial_narration": quest.initial_narration,
            "mission_description": quest.mission_description,
            "acts": [
                {"objective": act.objective, "scenes": act.scenes}
                for act in quest.acts
            ],
        }
