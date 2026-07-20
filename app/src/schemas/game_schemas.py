from pydantic import BaseModel

from src.game_engine.roll import ParticipantRoll
from src.game_engine.types import SceneType

class SceneResponse(BaseModel):
    narration: str
    scene_type: SceneType
    enemies: list[str]
    dialogue: list[dict[str, str]]
    game_id: int | None = None
    quest_id: int | None = None

class DialogueResponse(BaseModel):
    text: str
    npc: str

class InitiativeResponse(BaseModel):
    participant_rolls: list[ParticipantRoll]
