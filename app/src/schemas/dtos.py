from pydantic import BaseModel
from src.game_engine.types import CombatActionType


class PlayerActionDTO(BaseModel):
    action: CombatActionType
    roll: int
    target_enemy_id: int | None = None


class EnemyActionDTO(BaseModel):
    action: CombatActionType
    description: str | None = None
    damage: int | None = None
    succeeded: bool
