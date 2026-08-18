from pydantic import BaseModel

from src.game_engine.types import SceneType, CombatActionType
from src.schemas.dtos import EnemyActionDTO


class SceneResponse(BaseModel):
    narration: str
    scene_type: SceneType
    enemies: list[str]
    dialogue: list[dict[str, str]]
    game_id: int | None = None
    quest_id: int | None = None
    options: list[dict[str, str]] | None = None


class AnswerDialogueRequest(BaseModel):
    quest_id: int
    chosen_next_scene_id: str
    starts_quest: bool

class DialogueResponse(BaseModel):
    text: str
    npc: str


class EnemyListResponse(BaseModel):
    enemies: list[dict]


class EnemyActionsResponse(BaseModel):
    enemy_actions: list[EnemyActionDTO]


class PlayerActionRequest(BaseModel):
    quest_id: int
    action: CombatActionType
    roll: int
    target_enemy_id: int | None = None
    

class PlayerDamageRollRequest(BaseModel):
    quest_id: int
    total_damage: int # Takes the sum of the damage rolls and the fixed damage
    target_enemy_id: int | None = None
