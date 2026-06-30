from typing import Any

from .scene import Scene

class Act:
    objective: str
    scenes: list[Scene]

    def __init__(self, act_data: dict[str, Any]):
        self.objective = act_data.get("objective")
        self.scenes = [Scene(scene) for scene in act_data.get("scenes")]
