from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Enemy(Base):
    __tablename__ = "enemies"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    hp = Column(Integer, nullable=False)
    ac = Column(Integer, nullable=False)
    attacks = Column(String, nullable=False)
    encounter_id = Column(Integer, ForeignKey("encounters.id"))
    encounter = relationship("Encounter", back_populates="enemies")