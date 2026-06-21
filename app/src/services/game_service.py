from src.game import Game
from src.repositories.game_repository import GameRepository


class GameService:
    def __init__(self, game_repository: GameRepository, game_data: dict):
        self.game_repository = game_repository
        self.game_data = game_data

    def create_game(self, user_id: int) -> Game:
        db_game = self.game_repository.create_game(user_id)
        return Game(self.game_data, game_id=db_game.id)
