from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="characters")
    game_id = Column(Integer, ForeignKey("games.id"))
    game = relationship("Game", back_populates="characters")
    
    # General data
    name = Column(String, nullable=False)
    character_class = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    race = Column(String, nullable=False)
    background = Column(String, nullable=False)
    alignment = Column(String, nullable=False)
    player_name = Column(String, nullable=False)
    weapon = Column(String, nullable=False)
    armor = Column(String, nullable=False)
    
    # Attributes
    hp = Column(Integer, nullable=False)
    constitution = Column(Integer, nullable=False)
    dexterity = Column(Integer, nullable=False)
    strength = Column(Integer, nullable=False)
    wisdom = Column(Integer, nullable=False)
    intelligence = Column(Integer, nullable=False)
    charisma = Column(Integer, nullable=False)
