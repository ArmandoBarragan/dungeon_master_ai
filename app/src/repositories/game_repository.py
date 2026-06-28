from sqlalchemy.orm import Session

from src.models import Game


class GameRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_game(self, game_id: int) -> Game:
        return self.db.query(Game).filter(Game.id == game_id).first()

    def create_game(self, user_id: int) -> Game:
        game = Game(user_id=user_id)
        self.db.add(game)
        self.db.flush()
        self.db.refresh(game)
        return game

    def update_game(self, game: Game) -> Game:
        self.db.flush()
        return game