from enum import Enum

class SceneType(Enum):
    COMBAT = "combat"
    DIALOGUE = "dialogue"


class CombatActionType(str, Enum):
    # Ofensivas
    ATTACK = "attack"
    CAST_SPELL = "cast_spell"
    USE_SKILL = "use_skill"
