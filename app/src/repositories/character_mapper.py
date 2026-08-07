from src.models.character_model import Character
from src.schemas.character_schema import CharacterSchema


class CharacterMapper:

    @staticmethod
    def to_model(character: CharacterSchema,user_id: int,game_id: int,) -> Character:

        return Character(
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
            charisma=character.charisma,
        )