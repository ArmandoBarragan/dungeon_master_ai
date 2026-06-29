from src.game import Game
from src.repositories import GameRepository, QuestRepository, CharacterRepository
from src.game_engine.scene import Scene
from src.game_engine.quest import Quest
from src.models.quest_model import QuestStatus

class GameService:
    def __init__(
        self,
        game_repository: GameRepository,
        quest_repository: QuestRepository,
        character_repository: CharacterRepository,
    ):
        self.game_repository = game_repository
        self.quest_repository = quest_repository
        self.character_repository = character_repository

    def create_game(self, user_id: int) -> tuple[Game, int, int]:
        game = Game()
        db_game = self.game_repository.create_game(user_id)
        quest = game.quests[0]
        db_quest = self.quest_repository.create_quest(
            db_game.id, quest.story_key, quest.name, quest.description
        )
        character = game.character
        db_character = self.character_repository.create_character(user_id,db_game.id, character)
        db_game.active_quest_id = db_quest.id
        self.game_repository.update_game(db_game)
        return game, db_game.id, db_quest.id

    def get_latest_scene(self, quest_id: int) -> Scene | None:
        quest_record = self.quest_repository.get_quest(quest_id)
        if not quest_record:
            return None
        quest_data = Quest(quest_record.story_key)
        act = quest_data.acts[quest_record.current_act_index]
        scene = act.scenes[quest_record.current_scene_index]
        return Scene(scene)

    def accept_quest(self, quest_id: int) -> None:
        quest_record = self.quest_repository.get_quest(quest_id)
        if not quest_record:
            return
        quest_record.status = QuestStatus.IN_PROGRESS.value
        self.quest_repository.update_quest(quest_record)

    def advance_scene(self, quest_id: int) -> Scene | None:
        quest_record = self.quest_repository.get_quest(quest_id)
        quest = Quest(quest_record.story_key)
        current_act_scene_length = len(
            quest.acts[quest_record.current_act_index].scenes
        )
        if quest_record.current_scene_index == current_act_scene_length - 1:
            if quest_record.current_act_index == len(quest.acts) - 1:
                quest_record.status = QuestStatus.COMPLETED.value
                self.quest_repository.update_quest(quest_record)
                return None
            quest_record.current_scene_index = 0
            quest_record.current_act_index += 1
        else:
            quest_record.current_scene_index += 1
        self.quest_repository.update_quest(quest_record)
        return Scene(
            quest.acts[
                quest_record.current_act_index
            ].scenes[quest_record.current_scene_index]
        )
    
