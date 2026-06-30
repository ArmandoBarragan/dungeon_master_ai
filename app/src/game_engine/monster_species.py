import json
from pathlib import Path
from typing import Any

GAME_DATA_PATH = Path(__file__).resolve().parent / "game_data.json"


class MonsterSpecies:
    name: str
    size: str
    behavior: str
    attacks: list[dict[str, Any]]

    def __init__(self, name: str):
        with open(GAME_DATA_PATH, encoding="utf-8") as f:
            game_data = json.load(f)
        monsters = game_data.get("monsters", {})
        monster_data = monsters.get(name)
        if not monster_data:
            raise ValueError(f"Monster data not found for name: {name}")
        self.name = name
        for field, value in monster_data.items():
            setattr(self, field, value)
