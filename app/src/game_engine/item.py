from typing import Any


class Item:
    name: str
    description: str
    value: int
    weight: int
    quantity: int
    effects: list[str]
    conditions: list[str]
    actions: list[str]

    def __init__(self, item_data: dict[str, Any]):
        for field, value in item_data.items():
            setattr(self, field, value)