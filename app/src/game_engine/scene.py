from typing import Any

from .enemy import Enemy
from .types import SceneType

class Scene:
    narration: str
    scene_type: SceneType
    dialogue: list[dict[str, str]]
    enemies: list[Enemy]

    def __init__(self, scene_data: dict[str, Any] | None = None):
        scene_data = scene_data or {}
        self.narration = scene_data.get("narration")
        self.scene_type = SceneType(scene_data.get("type", SceneType.DIALOGUE.value))
        self.dialogue = scene_data.get("dialogue", [])
        self.enemies = [
            Enemy(enemy)
            for enemy in scene_data.get("enemies", [])
        ]
