from pydantic import BaseModel

class ParticipantRoll(BaseModel):
    """
    A participant roll is a roll made by a participant in an encounter.
    It can be a player or an enemy.
    """
    name: str
    enemy_id: int | None = None
    roll: int
