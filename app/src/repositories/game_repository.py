from sqlalchemy.orm import Session

from src.models import Game


class GameRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_game(self, user_id: int) -> Game:
        game = Game(user_id=user_id)
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        return game

    def update_game(self, game: Game) -> Game:
        self.db.commit()
        self.db.refresh(game)
        return game