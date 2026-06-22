from sqlalchemy.orm import Session
from src.models.quest_model import Quest as QuestModel


class QuestRepository:
    def __init__(self, db: Session):
        self.db = db

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
        self.db.commit()
        self.db.refresh(quest)
        return quest