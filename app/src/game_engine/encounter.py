from typing import Any

from .enemy import Enemy

class Encounter:
    enemies: list[Enemy]

    def __init__(self, encounter_data: dict[str, Any]):
        self.enemies = [Enemy(enemy) for enemy in encounter_data.get("enemies")]