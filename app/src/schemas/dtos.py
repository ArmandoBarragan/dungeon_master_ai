from pydantic import BaseModel
from src.game_engine.types import CombatActionType


class CharacterDTO(BaseModel):
    name: str
    character_class: str
    level: int
    race: str
    background: str
    alignment: str
    player_name: str
    weapon: str
    armor: str
    armor_class: int

    # Attributes
    max_hp: int
    current_hp: int
    constitution: int
    dexterity: int
    strength: int
    wisdom: int
    intelligence: int
    charisma: int


class PlayerActionDTO(BaseModel):
    action: CombatActionType
    roll: int
    target_enemy_id: int | None = None


class EnemyActionDTO(BaseModel):
    action: CombatActionType
    description: str | None = None
    damage: int | None = None
    succeeded: bool
