class Game:
    def __init__(self, character):
        self.character = character
        self.quests = []
        self.current_encounter_index = 0
    
    def start_quest(self):
        # 1. Generate first encouter
        # 2. Generate second encounter
        # 3. Generate boss encounter
        pass # This method starts a quest, creating three random encounters