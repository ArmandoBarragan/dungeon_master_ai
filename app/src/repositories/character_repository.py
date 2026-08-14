from sqlalchemy.orm import Session

from src.models.character_model import Character
from src.models.quest_model import Quest

class CharacterRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_character(self, character: Character) -> Character:
        self.db.add(character)
        self.db.flush()
        self.db.refresh(character)
        return character

    def get_character_from_quest(self, quest_id: int) -> Character | None:
        game_id = self.db.query(Quest).filter(Quest.id == quest_id).first().game.id
        return self.db.query(Character).filter(Character.game_id == game_id).first()

    def update(self, character: Character) -> Character:
        self.db.flush()
        return character
