from typing import Any


class Act:
    objective: str
    scenes: list[dict[str, Any]]

    def __init__(self, act_data: dict[str, Any]):
        self.objective = act_data.get("objective")
        self.scenes = act_data.get("scenes")
