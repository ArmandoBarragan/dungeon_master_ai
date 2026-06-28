from pydantic import BaseModel

from src.game_engine.types import SceneType

class SceneResponse(BaseModel):
    narration: str
    scene_type: SceneType
    enemies: list[str]
    dialogue: list[dict[str, str]]
