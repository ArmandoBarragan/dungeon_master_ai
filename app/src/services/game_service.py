import random

from dataclasses import dataclass, field
from src.models.enemy_model import Enemy as EnemyModel
from src.game import Game
from src.game_engine import Scene, Quest, ParticipantRoll, Enemy
from src.models import Character as CharacterModel, Game as GameModel
from src.models.encounter_model import Encounter as EncounterModel
from src.models.quest_model import Quest as QuestModel, QuestStatus
from src.repositories import (
    CharacterRepository,
    EncounterRepository,
    GameRepository,
    QuestRepository,
    EnemyRepository,
)


def _model_name(value) -> str:
    if isinstance(value, str):
        return value
    return value.name


@dataclass
class EnemyView:
    engine: Enemy
    db_id: int | None = None


@dataclass
class SceneContext:
    quest_id: int
    act_index: int
    scene_index: int
    scene: Scene
    encounter_id: int | None = None
    enemies: list[EnemyView] = field(default_factory=list)

    def _match_enemies_by_name(self, enemies: list[Enemy], enemy_records: list[EnemyModel]) -> list[EnemyView]:
        return [
            EnemyView(engine=enemy, db_id=enemy_record.id)
            for enemy in enemies for enemy_record in enemy_records
            if enemy.name == enemy_record.name
        ]

    def load_enemies(self, enemy_records: list[EnemyModel], scene: Scene) -> list[EnemyView]:
        return [
            EnemyView(engine=enemy, db_id=enemy_record.id)
            for enemy in scene.enemies for enemy_record in enemy_records
            if enemy.name == enemy_record.name
        ]


class GameService:
    def __init__(
        self,
        game_repository: GameRepository,
        quest_repository: QuestRepository,
        character_repository: CharacterRepository,
        encounter_repository: EncounterRepository,
        enemy_repository: EnemyRepository,
    ):
        self.game_repository = game_repository
        self.quest_repository = quest_repository
        self.character_repository = character_repository
        self.encounter_repository = encounter_repository
        self.enemy_repository = enemy_repository
    
    def _get_scene_context(self, quest_id: int) -> SceneContext | None:
        quest_record = self.quest_repository.get_quest(quest_id)
        if not quest_record:
            raise ValueError("Quest not found")
        quest = Quest(quest_record.story_key)
        scene = quest.get_current_scene(
            quest_record.current_act_index,
            quest_record.current_scene_index,
        )
        return SceneContext(
            quest_id=quest_id,
            act_index=quest_record.current_act_index,
            scene_index=quest_record.current_scene_index,
            scene=scene,
        )
        
    def create_game(self, user_id: int) -> tuple[Game, int, int]:
        game = Game()
        db_game = self.game_repository.create_game(GameModel(user_id=user_id))
        quest = game.quests[0]
        db_quest = self.quest_repository.create_quest(
            QuestModel(
                game_id=db_game.id,
                story_key=quest.story_key,
                name=quest.name,
                description=quest.description,
            )
        )
        character = game.character
        self.character_repository.create_character(
            CharacterModel(
                user_id=user_id,
                game_id=db_game.id,
                name=character.name,
                character_class=_model_name(character.character_class),
                level=character.level,
                race=_model_name(character.race),
                background=character.background,
                alignment=character.alignment,
                player_name=character.player_name,
                weapon=_model_name(character.weapon),
                armor=_model_name(character.armor),
                hp=character.hp,
                constitution=character.constitution,
                dexterity=character.dexterity,
                strength=character.strength,
                wisdom=character.wisdom,
                intelligence=character.intelligence,
                charisma=character.charisma,
            )
        )
        db_game.active_quest_id = db_quest.id
        self.game_repository.update_game(db_game)
        return game, db_game.id, db_quest.id

    def get_latest_scene(self, quest_id: int) -> Scene:
        quest_record = self.quest_repository.get_quest(quest_id)
        if not quest_record:
            raise ValueError("Quest not found")
        quest_data = Quest(quest_record.story_key)
        return quest_data.get_current_scene(
            quest_record.current_act_index,
            quest_record.current_scene_index
        )

    def accept_quest(self, quest_id: int):
        quest_record = self.quest_repository.get_quest(quest_id)
        if not quest_record:
            raise ValueError("Quest not found")
        quest_record.status = QuestStatus.IN_PROGRESS.value
        self.quest_repository.update_quest(quest_record)

    def advance_scene(self, quest_id: int) -> Scene | None:
        scene_context = self._get_scene_context(quest_id)
        quest_record = self.quest_repository.get_quest(scene_context.quest_id)
        quest = Quest(quest_record.story_key)
        current_act_scene_length = len(
            quest.acts[quest_record.current_act_index].scenes
        )
        if quest_record.current_scene_index == current_act_scene_length - 1:
            if quest_record.current_act_index == len(quest.acts) - 1:
                quest_record.status = QuestStatus.COMPLETED.value
                self.quest_repository.update_quest(quest_record)
                return None
            quest_record.current_act_index += 1
            quest_record.current_scene_index = 0
        else:
            quest_record.current_scene_index += 1
        self.quest_repository.update_quest(quest_record)
        return quest.get_current_scene(
            quest_record.current_act_index,
            quest_record.current_scene_index
        )

    def initiative_rolls(self, quest_id: int, player_roll: int) -> list[ParticipantRoll]:
        scene_context = self._get_scene_context(quest_id)
        if self.encounter_repository.get_current_encounter_by_quest_id(quest_id):
            raise ValueError("Encounter already exists for this quest")
        initiative_rolls = [ParticipantRoll(name="Player", enemy_id=None, roll=player_roll)]
        encounter = self.encounter_repository.create_encounter(
            EncounterModel(
                quest_id=quest_id,
                act_index=scene_context.act_index,
                scene_index=scene_context.scene_index,
            )
        )
        enemies = [
            EnemyModel(max_hp=enemy.max_hp, name=enemy.name, encounter_id=encounter.id)
            for enemy in scene_context.scene.enemies
        ]
        enemy_records = self.enemy_repository.create_enemies(enemies)
        for enemy in enemy_records:
            initiative = random.randint(1, 20)
            initiative_rolls.append(
                ParticipantRoll(name=enemy.name, enemy_id=enemy.id, roll=initiative)
            )

        return sorted(initiative_rolls, key=lambda x: x.roll, reverse=True)
