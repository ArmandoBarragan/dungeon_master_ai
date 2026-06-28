from typing import Any


class Attack:
    name: str
    damage: str

    def __init__(self, attack_data: dict[str, Any]):
        self.name = attack_data.get("name")
        self.damage = attack_data.get("damage")
