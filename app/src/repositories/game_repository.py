from sqlalchemy.orm import Session

from src.models import Game


class GameRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_game(self, game_id: int) -> Game | None:
        return self.db.query(Game).filter(Game.id == game_id).first()

    def get_games_by_user(self, user_id: int) -> list[Game]:
        return self.db.query(Game).filter(Game.user_id == user_id).all()

    def create_game(self, game: Game) -> Game:
        self.db.add(game)
        self.db.flush()
        self.db.refresh(game)
        return game

    def update_game(self, game: Game) -> Game:
        self.db.flush()
        return game
