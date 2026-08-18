from typing import Any

from .dialogue import Dialogue
from .enemy import Enemy
from .types import SceneType


class Scene:
    id: str
    narration: str
    scene_type: SceneType
    dialogue: list[Dialogue]
    enemies: list[Enemy]
    options: list[dict[str, str]]
    outcomes: list[dict[str, str]]

    def __init__(self, scene_data: dict[str, Any] | None = None):
        scene_data = scene_data or {}
        self.id = scene_data.get("id")
        self.narration = scene_data.get("narration")
        self.scene_type = SceneType(scene_data.get("type", SceneType.DIALOGUE.value))
        self.dialogue = scene_data.get("dialogue", [])
        self.options = scene_data.get("options", [])
        self.outcomes = scene_data.get("outcomes")
        self.enemies = [
            Enemy(enemy)
            for enemy in scene_data.get("enemies", [])
        ]
