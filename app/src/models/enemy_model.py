from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Enemy(Base):
    __tablename__ = "enemies"

    id = Column(Integer, primary_key=True)

    encounter_id = Column(Integer, ForeignKey("encounters.id"), nullable=False)
    encounter = relationship(
        "Encounter",
        back_populates="enemies",
        foreign_keys=[encounter_id],
    )

    name = Column(String, nullable=False)
    max_hp = Column(Integer)
    armor_class = Column(Integer)
    current_hp = Column(Integer)
