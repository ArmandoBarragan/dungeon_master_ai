import random

from src.game import Game
from src.repositories import GameRepository, QuestRepository
from src.game_engine.scene import Scene
from src.game_engine.quest import Quest
from src.models.quest_model import QuestStatus

class GameService:
    def __init__(
        self,
        game_repository: GameRepository,
        quest_repository: QuestRepository,
    ):
        self.game_repository = game_repository
        self.quest_repository = quest_repository

    def create_game(self, user_id: int) -> tuple[Game, int, int]:
        game = Game()
        db_game = self.game_repository.create_game(user_id)
        quest = game.quests[0]
        db_quest = self.quest_repository.create_quest(
            db_game.id, quest.story_key, quest.name, quest.description
        )
        db_game.active_quest_id = db_quest.id
        self.game_repository.update_game(db_game)
        return game, db_game.id, db_quest.id

    def get_latest_scene(self, quest_id: int) -> Scene | None:
        quest_record = self.quest_repository.get_quest(quest_id)
        if not quest_record:
            return None
        quest_data = Quest(quest_record.story_key)
        return quest_data.get_current_scene(
            quest_record.current_act_index,
            quest_record.current_scene_index
        )

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
        return quest.get_current_scene(
            quest_record.current_act_index,
            quest_record.current_scene_index
        )

    def initiative_roll(self, quest_id: int) -> dict[str, int]:
        quest_record = self.quest_repository.get_quest(quest_id)
        if not quest_record:
            return {}
        quest = Quest(quest_record.story_key)
        scene = quest.get_current_scene(
            quest_record.current_act_index,
            quest_record.current_scene_index
        )
        initiative_roles = {}
        for enemy in scene.enemies:
            initiative_roles[enemy.name] = random.randint(1, 20)
        return {
            enemy: initiative
            for enemy, initiative in sorted(initiative_roles.items(),
            key=lambda x: x[1], reverse=True)
        }
