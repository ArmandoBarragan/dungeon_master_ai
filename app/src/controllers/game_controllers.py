from fastapi import APIRouter, Depends

from src.dependencies import get_current_user_id, get_game_service
from src.services.game_service import GameService

router = APIRouter(prefix="/game", tags=["game"])


@router.post("/new_game/", status_code=201)
async def new_game(
    user_id: int = Depends(get_current_user_id),
    game_service: GameService = Depends(get_game_service),
):
    game = game_service.create_game(user_id)
    return {
        "initial_narration": game.quests[0].initial_narration,
        "incident_dialogue": game.quests[0].incident_dialogue,
    }
