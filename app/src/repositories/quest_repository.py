from sqlalchemy.orm import Session
from src.models.quest_model import Quest as QuestModel, QuestStatus


class QuestRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_active_quest_by_game_id(self, game_id: int) -> QuestModel | None:
        return self.db.query(QuestModel).filter(
            QuestModel.game_id == game_id,
            QuestModel.status == QuestStatus.IN_PROGRESS.value
        ).first()

    def get_quest(self, quest_id: int) -> QuestModel | None:
        return self.db.query(QuestModel).filter(QuestModel.id == quest_id).first()

    def create_quest(self,
        game_id: int,
        story_key: str,
        name: str,
        description: str,
    ) -> QuestModel:
        quest = QuestModel(
            game_id=game_id,
            story_key=story_key,
            name=name,
            description=description,
        )
        self.db.add(quest)
        self.db.flush()
        self.db.refresh(quest)
        return quest

    def update_quest(self, quest: QuestModel) -> QuestModel:
        self.db.flush()
        return quest
