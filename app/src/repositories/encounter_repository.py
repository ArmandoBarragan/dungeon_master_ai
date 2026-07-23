from sqlalchemy.orm import Session

from src.models.encounter_model import Encounter, EncounterStatus


class EncounterRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_encounter(self, encounter: Encounter) -> Encounter:
        self.db.add(encounter)
        self.db.flush()
        self.db.refresh(encounter)
        return encounter

    def get_current_encounter_by_quest_id(self, quest_id: int) -> Encounter | None:
        return self.db.query(Encounter).filter(
            Encounter.quest_id == quest_id,
            Encounter.state == EncounterStatus.ACTIVE.value,
        ).first()

    def get_encounter(self, encounter_id: int) -> Encounter | None:
        return self.db.query(Encounter).filter(Encounter.id == encounter_id).first()

    def update_encounter(self, encounter: Encounter) -> Encounter:
        self.db.flush()
        return encounter
