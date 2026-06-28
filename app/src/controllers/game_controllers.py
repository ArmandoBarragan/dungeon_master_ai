from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import get_current_user_id, get_game_service
from src.game_engine.types import SceneType
from src.services.game_service import GameService
from src.schemas import SceneResponse

router = APIRouter(prefix="/game", tags=["game"])


@router.post("/new_game/", status_code=201)
async def new_game(
    user_id: int = Depends(get_current_user_id),
    game_service: GameService = Depends(get_game_service),
):
    game = game_service.create_game(user_id)
    intro_scene = game.quests[0].acts[0].scenes[0]
    return SceneResponse(
        narration=intro_scene.get("narration"),
        scene_type=SceneType.DIALOGUE,
        enemies=[],
        dialogue=intro_scene.get("dialogue", []),
    )

@router.get("/get_latest_scene/", status_code=200)
async def get_latest_scene(
    game_id: int,
    game_service: GameService = Depends(get_game_service),
):
    scene = game_service.get_latest_scene(game_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene or game not found")
    dialogue = scene.dialogue if scene.scene_type == SceneType.DIALOGUE else []
    return SceneResponse(
        narration=scene.narration,
        scene_type=scene.scene_type,
        enemies=[enemy.species.name for enemy in scene.enemies],
        dialogue=dialogue,
    )

@router.post("/answer_dialogue/", status_code=200)
async def answer_dialogue(
    quest_id: int,
    game_service: GameService = Depends(get_game_service),
):
    answer_dialogue = "Yes, and I will help you." # Turn this later into a prompt
    user_accepted = True
    game_service.advance_scene(quest_id)
    scene = game_service.get_latest_scene(quest_id)
    return SceneResponse(
        narration=scene.narration,
        scene_type=scene.scene_type,
        enemies=[enemy.species.name for enemy in scene.enemies],
        dialogue=scene.dialogue if scene.scene_type == SceneType.DIALOGUE else [],
    )
