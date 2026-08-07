from pydantic import BaseModel, Field


class CharacterCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    character_class: str
    level: int
    race: str
    background: str
    alignment: str
    player_name: str
    weapon: str
    armor: str
    hp: int
    constitution:   int
    dexterity:  int
    strength:   int
    wisdom: int
    intelligence:   int
    charisma:   int