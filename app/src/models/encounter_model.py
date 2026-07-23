from enum import Enum

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base


class EncounterStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"


class Encounter(Base):
    __tablename__ = "encounters"

    id = Column(Integer, primary_key=True)
    quest_id = Column(Integer, ForeignKey("quests.id"), nullable=False)
    quest = relationship(
        "Quest",
        back_populates="encounters",
        foreign_keys=[quest_id],
    )

    act_index = Column(Integer, nullable=False)
    scene_index = Column(Integer, nullable=False)
    state = Column(String, nullable=False, default=EncounterStatus.ACTIVE.value)
    enemies = relationship("Enemy", back_populates="encounter")
