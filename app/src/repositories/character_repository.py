from sqlalchemy.orm import Session
from src.models.character_model import Character as CharacterModel
from src.game_engine.character import Character


class CharacterRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_character(self, 
        user_id:int, 
        game_id: int,
        character: Character,
    ) -> CharacterModel:
        character_db = CharacterModel(
            user_id=user_id,
            game_id=game_id,
            name=character.name,
            character_class=character.character_class,
            level=character.level,
            race=character.race,
            background=character.background,
            alignment=character.alignment,
            player_name=character.player_name,
            weapon=character.weapon,
            armor=character.armor,
            hp=character.hp,
            constitution=character.constitution,
            dexterity=character.dexterity,
            strength=character.strength,
            wisdom=character.wisdom,
            intelligence=character.intelligence,
            charisma=character.charisma
        )
        self.db.add(character_db)
        self.db.flush()
        self.db.refresh(character_db)
        return character_db

    def get_character(self, character_id: int) -> CharacterModel | None:
        return self.db.query(CharacterModel).filter(CharacterModel.id == character_id).first()

    def update_character(self, character: CharacterModel) -> CharacterModel:
        self.db.flush()
        return character
