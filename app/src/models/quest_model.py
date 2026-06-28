from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base
from enum import Enum

class QuestStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    game = relationship(
        "Game",
        back_populates="quests",
        foreign_keys=[game_id],
    )
    story_key = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, default=QuestStatus.NOT_STARTED.value, nullable=False)
    current_act_index = Column(Integer, default=0, nullable=False)
    current_scene_index = Column(Integer, default=0, nullable=False)
