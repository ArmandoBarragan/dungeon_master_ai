class Quest:
    def __init__(self, name, description, reward, boss, location):
        self.name = name
        self.description = description
        self.reward = reward
        self.boss = boss
        self.location = location

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "reward": self.reward,
            "boss": self.boss,
            "location": self.location,
        }
    
    def description_quest(self):
    
        return f"""
        Mision: {self.name}

        {self.description}

        Location: {self.location}
        Final Boss: {self.boss}
        Reward: {self.reward}
        
        "Héroe... destiny calls you. You must travel to {self.location} and face {self.boss}.
        Only then will you be able to claim {self.reward}... if you survive."

        """
