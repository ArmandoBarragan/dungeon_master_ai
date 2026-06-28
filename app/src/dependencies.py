from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from config.db import get_db
from src.repositories import GameRepository, QuestRepository, UserRepository
from src.services.auth_service import AuthService
from src.services.game_service import GameService

bearer_scheme = HTTPBearer()


def get_game_data(request: Request) -> dict:
    return request.app.state.game_rules


def get_game_repository(db: Session = Depends(get_db)) -> GameRepository:
    return GameRepository(db)


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_quest_repository(db: Session = Depends(get_db)) -> QuestRepository:
    return QuestRepository(db)

def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository)


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> int:
    try:
        return auth_service.get_user_id(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def get_game_service(db: Session = Depends(get_db)) -> GameService:
    return GameService(
        GameRepository(db),
        QuestRepository(db),
    )
