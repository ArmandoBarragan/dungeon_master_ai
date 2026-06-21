from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="games")
    characters = relationship("Character", back_populates="game")
    encounters = relationship("Encounter", back_populates="game")
    quests = relationship("Quest", back_populates="game")
