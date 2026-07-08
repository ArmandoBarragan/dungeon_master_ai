from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import get_current_user_id, get_game_service
from src.game_engine import Scene
from src.game_engine.types import SceneType
from src.services.game_service import GameService
from src.schemas import SceneResponse, DialogueResponse, InitiativeResponse

router = APIRouter(prefix="/game", tags=["game"])


def _to_scene_response(scene: Scene, quest_id: int, game_id: int | None = None) -> SceneResponse:
    return SceneResponse(
        narration=scene.narration,
        scene_type=scene.scene_type,
        enemies=[enemy.name for enemy in scene.enemies],
        dialogue=scene.dialogue if scene.scene_type == SceneType.DIALOGUE else [],
        game_id=game_id,
        quest_id=quest_id,
    )

@router.post("/new_game/", status_code=201)
async def new_game(
    user_id: int = Depends(get_current_user_id),
    game_service: GameService = Depends(get_game_service),
):
    game, game_id, quest_id = game_service.create_game(user_id)
    intro_scene = game.quests[0].acts[0].scenes[0]
    return _to_scene_response(intro_scene, quest_id, game_id)

@router.get("/get_latest_scene/", status_code=200)
async def get_latest_scene(
    quest_id: int,
    game_service: GameService = Depends(get_game_service),
):
    scene = game_service.get_latest_scene(quest_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene or quest not found")
    dialogue = scene.dialogue if scene.scene_type == SceneType.DIALOGUE else []
    return _to_scene_response(scene, quest_id)

@router.post("/answer_dialogue/", status_code=200)
async def answer_dialogue(
    quest_id: int,
    game_service: GameService = Depends(get_game_service),
):
    game_service.accept_quest(quest_id)
    return DialogueResponse(
        text="Great, thanks!",
        npc="The innkeeper",
    )

@router.post("/advance_scene/", status_code=200)
async def advance_scene(
    quest_id: int,
    game_service: GameService = Depends(get_game_service),
):
    game_service.advance_scene(quest_id)
    scene = game_service.get_latest_scene(quest_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene or quest not found")
    return _to_scene_response(scene, quest_id)

@router.post("/initiative_roll/", status_code=200)
async def initiative_roll(
    quest_id: int,
    roll: int,
    game_service: GameService = Depends(get_game_service),
):
    enemy_initiative_rolls = game_service.initiative_roll(quest_id)
    if not enemy_initiative_rolls:
        raise HTTPException(status_code=404, detail="Scene or quest not found")
    return InitiativeResponse(
        enemy_initiative_rolls=enemy_initiative_rolls,
        player_roll=roll,
    )
