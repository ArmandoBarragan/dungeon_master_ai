from . import Enemy
from enum import Enum
from typing import Any

class SceneType(Enum):
    COMBAT = "combat"
    DIALOGUE = "dialogue"

class Scene:
    narration: str
    scene_type: SceneType
    enemies: list[Enemy]

    def __init__(self, scene_data: dict[str, Any]):
        self.narration = scene_data.get("narration")
        self.scene_type = SceneType(scene_data.get("type"))
        self.enemies = [
            Enemy(enemy) 
            for enemy in scene_data.get("enemies")
        ]
