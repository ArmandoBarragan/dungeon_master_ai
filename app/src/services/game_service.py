import random

from dataclasses import dataclass, field
from pydantic import BaseModel, ConfigDict

from src.game import Game
from src.game_engine import Scene, Quest, Enemy, CombatActionType, Dialogue
from src.models import Character as CharacterModel, Game as GameModel, Enemy as EnemyModel
from src.models.encounter_model import Encounter as EncounterModel, EncounterStatus
from src.models.quest_model import Quest as QuestModel, QuestStatus
from src.repositories import (
    CharacterRepository,
    EncounterRepository,
    GameRepository,
    QuestRepository,
    EnemyRepository,
)
from src.schemas.dtos import PlayerActionDTO, EnemyActionDTO, CharacterDTO


def _model_name(value) -> str:
    if isinstance(value, str):
        return value
    return value.name


class EnemyView(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    engine: Enemy
    record: EnemyModel


@dataclass
class SceneContext:
    quest_id: int
    scene_index: int
    scene: Scene
    encounter_id: int | None = None
    enemies: list[EnemyView] = field(default_factory=list)

    def load_enemies(self, enemy_records: list[EnemyModel], player_turn: int) -> list[EnemyView]:
        """Pair encounter records with their quest-defined enemy engines by key."""
        enemies_by_key = {enemy.key: enemy for enemy in self.scene.enemies}
        enemy_views = []

        for enemy_record in enemy_records:
            engine = enemies_by_key.get(enemy_record.key)
            if engine is None:
                raise ValueError(
                    f"Enemy key '{enemy_record.key}' is not defined in scene "
                    f"'{self.scene.id}'."
                )
            enemy_views.append(EnemyView(engine=engine, record=enemy_record))

        self.enemies = enemy_views
        enemy_views = sorted(
            enemy_views, key=lambda x: x.record.initiative_turn, reverse=False
        )
        enemy_views = enemy_views[player_turn:] + enemy_views[:player_turn]
        return enemy_views


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
        scene = quest.get_scene(quest_record.scene_id)
        if scene is None:
            raise ValueError(
                f"Scene not found for quest: {quest_record.scene_id}"
            )
        scene_index = next(
            index for index, quest_scene in enumerate(quest.scenes)
            if quest_scene.id == scene.id
        )
        return SceneContext(
            quest_id=quest_id,
            scene_index=scene_index,
            scene=scene,
        )
        
    def create_game(self, user_id: int, world_name: str) -> tuple[Game, int, int]:
        game = Game()
        db_game = self.game_repository.create_game(GameModel(user_id=user_id, world_name=world_name))
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
                max_hp=character.max_hp,
                current_hp=character.max_hp,
                constitution=character.constitution,
                dexterity=character.dexterity,
                strength=character.strength,
                wisdom=character.wisdom,
                intelligence=character.intelligence,
                charisma=character.charisma,
                armor_class=10,
            )
        )
        db_game.active_quest_id = db_quest.id
        self.game_repository.update_game(db_game)
        return game, db_game.id, db_quest.id

    def get_games(self, user_id: int) -> list[dict[str, int]]:
        games = self.game_repository.get_games_by_user(user_id)
        games = [(game, game.characters[0]) for game in games]
        return [
            {
                "game_id": game.id,
                "character_name": character.name,
                "world_name": game.world_name,
                "active_quest_id": game.active_quest_id,
            }
            for game, character in games
        ]

    def get_character(self, game_id: int) -> CharacterDTO:
        character_record = self.character_repository.get_character_from_game(game_id)
        if not character_record:
            raise ValueError("Character not found for this game.")
        return CharacterDTO(
            name=character_record.name,
            character_class=character_record.character_class,
            level=character_record.level,
            race=character_record.race,
            background=character_record.background,
            alignment=character_record.alignment,
            player_name=character_record.player_name,
            weapon=character_record.weapon,
            armor=character_record.armor,
            armor_class=character_record.armor_class,
            max_hp=character_record.max_hp,
            current_hp=character_record.current_hp,
            constitution=character_record.constitution,
            dexterity=character_record.dexterity,
            strength=character_record.strength,
            wisdom=character_record.wisdom,
            intelligence=character_record.intelligence,
            charisma=character_record.charisma
        )

    def get_current_scene(self, quest_id: int) -> Scene:
        quest_record = self.quest_repository.get_quest(quest_id)
        if not quest_record:
            raise ValueError("Quest not found")
        quest = Quest(quest_record.story_key)
        return quest.get_scene(quest_record.scene_id)

    def answer_dialogue(
        self, quest_id: int, chosen_next_scene_id: str
    ) -> list[Dialogue]:
        quest_record = self.quest_repository.get_quest(quest_id)
        if not quest_record:
            raise ValueError("Quest not found")
        scene = Quest(quest_record.story_key).get_scene(quest_record.scene_id)
        if scene is None:
            raise ValueError(f"Scene not found for quest: {quest_record.scene_id}")
        option = next(
            (
                option
                for option in scene.options
                if option.next_scene_id == chosen_next_scene_id
            ),
            None,
        )
        if option is None:
            raise ValueError(
                f"Option not found for next scene: {chosen_next_scene_id}"
            )
        # Not all dialogues start quests but if they have that attribute as false and the quest
        # is already started, it would reset it to NOT STARTED, so we only update the attribute when
        # it's true
        if option.starts_quest:
            quest_record.status = QuestStatus.IN_PROGRESS.value
        quest_record.scene_id = chosen_next_scene_id
        self.quest_repository.update(quest_record)
        return option.npc_response

    def initiative_roll(self, quest_id: int, player_roll: int) -> list[dict[str, int]]:
        scene_context = self._get_scene_context(quest_id)        
        encounter_record = self.encounter_repository.get_current_encounter_by_quest_id(quest_id)
        if encounter_record:
            enemies = self.enemy_repository.get_enemies_by_encounter_id(encounter_record.id)
            return [{"name": enemy.name, "id": enemy.id} for enemy in enemies]

        encounter = self.encounter_repository.create_encounter(
            EncounterModel(
                quest_id=quest_id,
                scene_index=scene_context.scene_index,
            )
        )
        rolls = [(enemy, random.randint(1, 20)) for enemy in scene_context.scene.enemies]
        rolls.append((None, player_roll))
        rolls = sorted(
            rolls,
            key=lambda x: x[1],
            reverse=True,
        )
        enemies = []
        for i, (enemy, _) in enumerate(rolls):
            if enemy is None:
                encounter.player_initiative_turn = i
                self.encounter_repository.update(encounter)
                continue
            enemies.append(EnemyModel(
                max_hp=enemy.max_hp,
                name=enemy.name,
                encounter_id=encounter.id,
                initiative_turn=i,
                armor_class=enemy.armor_class,
                current_hp=enemy.max_hp,
                key=enemy.key,
            ))
        enemy_records = self.enemy_repository.create_enemies(enemies)
        return [{"name": enemy.name, "id": enemy.id} for enemy in enemy_records]

    def enemy_actions(self, quest_id: int, first_turn: bool) -> list[EnemyActionDTO]:
        encounter_record = self.encounter_repository.get_current_encounter_by_quest_id(quest_id)
        if not encounter_record:
            raise ValueError("No active encounter found for this quest.")
        
        enemy_records = self.enemy_repository.get_enemies_by_encounter_id(
            encounter_record.id,
            order_by=[("initiative_turn", "asc")],
        )

        scene_context = self._get_scene_context(quest_id)
        enemy_views = scene_context.load_enemies(enemy_records, encounter_record.player_initiative_turn)
        character = self.character_repository.get_character_from_game(encounter_record.quest.game_id)
        actions = []
        for enemy in enemy_views:
            attack_result = enemy.engine.play_turn(character.armor_class)
            if attack_result.get("succeeded"):
                character.current_hp -= attack_result.get("total_damage")
                if character.current_hp < 0:
                    character.current_hp = 0
            action = EnemyActionDTO(
                action=CombatActionType.ATTACK,
                attack_roll=attack_result.get("attack_roll"),
                damage=attack_result.get("total_damage"),
                succeeded=attack_result.get("succeeded"),
            )
            actions.append(action)
        self.character_repository.update(character)
        if character.current_hp <= 0:
            encounter_record.state = EncounterStatus.DEFEATED.value
            self.encounter_repository.update(encounter_record)
        return actions

    def player_action(self, quest_id: int, action: PlayerActionDTO) -> bool:
        encounter_record = self.encounter_repository.get_current_encounter_by_quest_id(quest_id)
        if not encounter_record:
            raise ValueError("No active encounter found for this quest.")
        
        character = self.character_repository.get_character_from_game(encounter_record.quest.game_id)
        if action.action == CombatActionType.ATTACK:
            target_enemy = self.enemy_repository.get(action.target_enemy_id)
            if not target_enemy or target_enemy.encounter_id != encounter_record.id:
                raise ValueError("Target enemy not found in the current encounter.")
            attack_roll = action.roll + character.strength
            return attack_roll > target_enemy.armor_class    
        else:
            raise NotImplementedError(f"Action {action.action} is not implemented yet.")

    def damage_roll(self, quest_id: int, total_damage: int, target_enemy_id: int) -> None:
        encounter_record = self.encounter_repository.get_current_encounter_by_quest_id(quest_id)
        if not encounter_record:
            raise ValueError("No active encounter found for this quest.")
        
        character = self.character_repository.get_character_from_game(encounter_record.quest.game_id)
        target_enemy = self.enemy_repository.get(target_enemy_id)
        if not target_enemy:
            raise ValueError("Target enemy not found in the current encounter.")
        
        target_enemy.current_hp -= total_damage
        if target_enemy.current_hp <= 0:
            self.enemy_repository.delete(target_enemy.id)
        else:
            self.enemy_repository.update(target_enemy)
        enemy_records = self.enemy_repository.get_enemies_by_encounter_id(encounter_record.id)
        if not enemy_records:
            encounter_record.state = EncounterStatus.SUCCEEDED.value
            self.encounter_repository.update(encounter_record)
        return [{"name": enemy.name, "id": enemy.id} for enemy in enemy_records]
 
    def forward_scene(self, quest_id: int) -> Scene:
        quest_record = self.quest_repository.get_quest(quest_id)
        if not quest_record:
            raise ValueError("Quest not found")

        quest = Quest(quest_record.story_key)
        current_scene = quest.get_scene(quest_record.scene_id)
        if current_scene is None:
            raise ValueError(f"Scene not found for quest: {quest_record.scene_id}")
        if not current_scene.outcomes:
            raise ValueError("Current scene has no outcomes")

        encounter = self.encounter_repository.get_latest_encounter_by_quest_id(quest_id)
        terminal_states = {
            EncounterStatus.SUCCEEDED.value,
            EncounterStatus.DEFEATED.value,
        }
        if not encounter or encounter.state not in terminal_states:
            raise ValueError("Encounter is not finished")

        character = self.character_repository.get_character_from_game(quest_record.game_id)
        enemies = self.enemy_repository.get_enemies_by_encounter_id(encounter.id)

        if encounter.state == EncounterStatus.SUCCEEDED.value and enemies:
            raise ValueError("Succeeded encounter still has living enemies")
        if encounter.state == EncounterStatus.DEFEATED.value and character.current_hp > 0:
            raise ValueError("Defeated encounter has a living character")

        outcome = next(
            (outcome for outcome in current_scene.outcomes
             if outcome.get("result") == encounter.state),
            None,
        )
        if outcome is None:
            raise ValueError(f"No outcome configured for result: {encounter.state}")

        next_scene = quest.get_scene(outcome.get("next_scene_id"))
        if next_scene is None:
            raise ValueError(
                f"Scene not found for outcome: {outcome.get('next_scene_id')}"
            )

        quest_record.scene_id = next_scene.id
        self.quest_repository.update(quest_record)
        return next_scene
