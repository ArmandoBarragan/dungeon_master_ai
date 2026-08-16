from typing import Any


class Attack:
    name: str
    roll_repetitions: int
    dice_type: int
    fixed_damage: int

    def __init__(self, attack_data: dict[str, Any]):
        self.name = attack_data.get("name")
        damage = attack_data.get("damage")
        self.roll_repetitions = damage.get("roll_repetitions")
        self.dice_type = damage.get("dice_type")
        self.fixed_damage = damage.get("fixed_damage")
