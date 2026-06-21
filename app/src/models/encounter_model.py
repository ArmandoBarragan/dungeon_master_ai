from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Encounter(Base):
    __tablename__ = "encounters"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    game = relationship("Game", back_populates="encounters")
    encounter_type = Column(String, nullable=False)
    enemies = relationship("Enemy", back_populates="encounter")
