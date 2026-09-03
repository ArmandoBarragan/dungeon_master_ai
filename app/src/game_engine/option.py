from .dialogue import Dialogue


class Option:
    text: str
    next_scene_id: str
    starts_quest: bool
    npc_response: list[Dialogue]

    def __init__(self, option_data: dict):
        self.text = option_data["text"]
        self.next_scene_id = option_data["next_scene_id"]
        self.starts_quest = option_data.get("starts_quest", False)
        self.npc_response = [
            Dialogue(response["npc"], response["dialogue"])
            for response in option_data.get("npc_response", [])
        ]
