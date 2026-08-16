from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import get_current_user_id, get_game_service
from src.game_engine import Scene
from src.game_engine.types import SceneType
from src.services.game_service import GameService
from src.schemas import (
    SceneResponse,
    DialogueResponse,
    EnemyActionsResponse,
    PlayerActionRequest,
    PlayerActionDTO,
    PlayerDamageRollRequest,
    EnemyListResponse,
)

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
    world_name: str,
    user_id: int = Depends(get_current_user_id),
    game_service: GameService = Depends(get_game_service),
):
    game, game_id, quest_id = game_service.create_game(user_id, world_name)
    intro_scene = game.quests[0].acts[0].scenes[0]
    return _to_scene_response(intro_scene, quest_id, game_id)


@router.get("/", status_code=200)
async def get_games(
        user_id: int = Depends(get_current_user_id),
        game_service: GameService = Depends(get_game_service)
    ):
    games = game_service.get_games(user_id)
    return {"games": games}


@router.get("/get_latest_scene/", status_code=200)
async def get_latest_scene(
    quest_id: int,
    game_service: GameService = Depends(get_game_service),
):
    try:
        scene = game_service.get_latest_scene(quest_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    dialogue = scene.dialogue if scene.scene_type == SceneType.DIALOGUE else []
    return _to_scene_response(scene, quest_id)

@router.get("/character/", status_code=200)
async def get_character(
    game_id: int,
    game_service: GameService = Depends(get_game_service),
):
    try:
        character = game_service.get_character(game_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return character

@router.post("/answer_dialogue/", status_code=200)
async def answer_dialogue(
    quest_id: int,
    game_service: GameService = Depends(get_game_service),
):
    try:
        game_service.accept_quest(quest_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return DialogueResponse(
        text="Great, thanks!",
        npc="The innkeeper",
    )

@router.post("/advance_scene/", status_code=200)
async def advance_scene(
    quest_id: int,
    game_service: GameService = Depends(get_game_service),
):
    try:
        scene = game_service.advance_scene(quest_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return _to_scene_response(scene, quest_id)

@router.post("/initiative_roll/", status_code=200)
async def initiative_roll(
    quest_id: int,
    roll: int,
    game_service: GameService = Depends(get_game_service),
):
    try:
        enemies = game_service.initiative_roll(quest_id, roll)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return EnemyListResponse(enemies=enemies)

@router.post("/enemy_actions/", status_code=200)
async def enemy_actions(
    quest_id: int,
    first_turn: bool,
    game_service: GameService = Depends(get_game_service),
):
    try:
        actions = game_service.enemy_actions(quest_id, first_turn)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return EnemyActionsResponse(enemy_actions=actions)

@router.post("/player_action/", status_code=200)
async def player_action(
    action: PlayerActionRequest,
    game_service: GameService = Depends(get_game_service),
):
    try:
        action_succeeded = game_service.player_action(
            action.quest_id,
            PlayerActionDTO(
                action=action.action,
                roll=action.roll,
                target_enemy_id=action.target_enemy_id,
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"action_succeeded": action_succeeded}

@router.post("/damage_roll/", status_code=200)
async def damage_roll(
    damage_roll: PlayerDamageRollRequest,
    game_service: GameService = Depends(get_game_service),
):
    try:
        enemies = game_service.damage_roll(
            damage_roll.quest_id,
            damage_roll.total_damage,
            damage_roll.target_enemy_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return EnemyListResponse(enemies=enemies)
