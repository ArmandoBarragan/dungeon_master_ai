from .dialogue import Dialogue

class Option:
    text: str
    next_scene_id: str
    starts_quest: str
    npc_response: Dialogue
