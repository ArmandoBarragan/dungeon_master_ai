from sqlalchemy.orm import Session

from src.models.character_model import Character


class CharacterRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_character(self, character: Character) -> Character:
        self.db.add(character)
        self.db.flush()
        self.db.refresh(character)
        return character

    def get_character(self, character_id: int) -> Character | None:
        return self.db.query(Character).filter(Character.id == character_id).first()

    def update_character(self, character: Character) -> Character:
        self.db.flush()
        return character
