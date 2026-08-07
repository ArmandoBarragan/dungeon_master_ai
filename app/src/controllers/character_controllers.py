from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.character_schema import CharacterCreate
from src.services.game_service import GameService
from src.dependencies import get_current_user_id, get_game_service, get_character_repository


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/create_character/", status_code=201)
async def create_character(
        character: CharacterCreate,
        game_id: int,
        user_id: int = Depends(get_current_user_id),
        game_service: GameService = Depends(get_game_service),
    ):
    try:
        game_service.create_character(user_id, game_id, character)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    return True
