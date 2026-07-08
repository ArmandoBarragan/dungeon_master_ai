import json
from pathlib import Path
from typing import Any

from .act import Act
from .scene import Scene

QUEST_DATA_PATH = Path(__file__).resolve().parents[3] / "writting" / "quest.json"


class Quest:
    name: str
    mission_description: dict[str, str]
    acts: list[Act]
    reward: dict[str, Any]
    story_key: str
    
    def __init__(self, story_key: str):
        quest_data = self._load_quest_data(story_key)
        self.name = quest_data.get("name")
        self.description = quest_data.get("description")
        self.story_key = quest_data.get("story_key")
        quest_data = quest_data.get("story")
        required_fields = [
            "mission_description",
            "acts",
            "reward",
        ]
        fields = [quest_data.get(field) for field in required_fields]
        if not all(fields):
            raise ValueError("Quest data is missing required fields")
        for field_name, field_value in zip(required_fields, fields):
            if field_name == "acts":
                setattr(self, field_name, [Act(act) for act in field_value])
                continue
            setattr(self, field_name, field_value)

    def _load_quest_data(self, story_key: str) -> dict[str, Any]:
        # TODO: Add S3 integration for production environment
        with open(QUEST_DATA_PATH, encoding="utf-8") as file:
            quests = json.load(file)
        quest_data = next((
            quest for quest in quests if quest.get("story_key") == story_key
        ), None)
        if not quest_data:
            raise ValueError(f"Quest data not found for story key: {story_key}")
        return quest_data

    def get_current_scene(self, current_act_index: int, current_scene_index: int) -> Scene:
        return self.acts[current_act_index].scenes[current_scene_index]
