from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    games = relationship("Game", back_populates="user")
    characters = relationship("Character", back_populates="user")
