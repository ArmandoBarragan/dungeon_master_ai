from sqlalchemy.orm import Session

from src.models.quest_model import Quest, QuestStatus


class QuestRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_active_quest_by_game_id(self, game_id: int) -> Quest | None:
        return self.db.query(Quest).filter(
            Quest.game_id == game_id,
            Quest.status == QuestStatus.IN_PROGRESS.value
        ).first()

    def get_quest(self, quest_id: int) -> Quest | None:
        return self.db.query(Quest).filter(Quest.id == quest_id).first()

    def create_quest(self, quest: Quest) -> Quest:
        self.db.add(quest)
        self.db.flush()
        self.db.refresh(quest)
        return quest

    def update_quest(self, quest: Quest) -> Quest:
        self.db.flush()
        return quest
