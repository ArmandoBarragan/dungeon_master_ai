import json
from pathlib import Path
from typing import Any

from .act import Act

QUEST_DATA_PATH = Path(__file__).resolve().parents[3] / "writting" / "quest.json"


class Quest:
    initial_narration: str
    incident_dialogue: list[dict[str, str]]
    mission_description: dict[str, str]
    acts: list[Act]
    final_dialogue: dict[str, str]
    reward: dict[str, Any]

    def __init__(self):
        quest_data = self._load_quest_data()
        required_fields = [
            "initial_narration",
            "incident_dialogue",
            "mission_description",
            "acts",
            "final_dialogue",
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

    def _load_quest_data(self) -> dict[str, Any]:
        # TODO: Add S3 integration for production environment
        with open(QUEST_DATA_PATH, encoding="utf-8") as file:
            return json.load(file)
