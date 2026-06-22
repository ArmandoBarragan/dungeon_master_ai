from src.game import Game
from src.repositories import GameRepository, QuestRepository


class GameService:
    def __init__(
        self,
        game_repository: GameRepository,
        quest_repository: QuestRepository,
        game_data: dict,
    ):
        self.game_repository = game_repository
        self.game_data = game_data
        self.quest_repository = quest_repository

    def create_game(self, user_id: int) -> Game:
        game = Game(self.game_data)
        db_game = self.game_repository.create_game(user_id)
        quest = game.quests[0]
        db_quest = self.quest_repository.create_quest(
            db_game.id, quest.story_key, quest.name, quest.description
        )
        db_game.active_quest_id = db_quest.id
        self.game_repository.update_game(db_game)
        return game
