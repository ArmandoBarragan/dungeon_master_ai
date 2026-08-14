import random

from dataclasses import dataclass, field
from src.models.enemy_model import Enemy as EnemyModel
from src.game import Game
from src.game_engine import Scene, Quest, Enemy, CombatActionType
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
from src.schemas import PlayerActionDTO, EnemyActionDTO


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

    def load_enemies(self, enemy_records: list[EnemyModel]) -> list[EnemyView]:
        return [
            EnemyView(engine=enemy, db_id=enemy_record.id)
            for enemy in self.scene.enemies for enemy_record in enemy_records
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
                armor_class=10,
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

    def initiative_roll(self, quest_id: int, player_roll: int) -> list[dict[str, int]]:
        scene_context = self._get_scene_context(quest_id)        
        encounter_record = self.encounter_repository.get_current_encounter_by_quest_id(quest_id)
        if encounter_record:
            enemies = self.enemy_repository.get_enemies_by_encounter_id(encounter_record.id)
            return [{"name": enemy.name, "id": enemy.id} for enemy in enemies]

        encounter = self.encounter_repository.create_encounter(
            EncounterModel(
                quest_id=quest_id,
                act_index=scene_context.act_index,
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
                self.encounter_repository.update_encounter(encounter)
                continue
            enemies.append(EnemyModel(
                max_hp=enemy.max_hp,
                name=enemy.name,
                encounter_id=encounter.id,
                initiative_turn=i,
                armor_class=enemy.armor_class,
                current_hp=enemy.max_hp,
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

        turns = [(enemy.name, enemy.initiative_turn) for enemy in enemy_records]
        turns.append(("player", encounter_record.player_initiative_turn))
        turns = sorted(turns, key=lambda x: x[1])
        
        player_turn = encounter_record.player_initiative_turn
        if first_turn:
            enemy_records = enemy_records[:player_turn]
        else:
            enemy_records = enemy_records[player_turn:] + enemy_records[:player_turn]
        actions = []

        scene_context = self._get_scene_context(quest_id)
        enemy_views = scene_context.load_enemies(enemy_records)
        character = self.character_repository.get_character_from_quest(quest_id)
        character_armor_class = character.armor_class
        for enemy in enemy_views:
            attack_roll = random.randint(1, 20)
            total_damage = 0
            description = f"{enemy.engine.name} attacks you."
            attack = enemy.engine.attacks[0]
            if attack_roll > character_armor_class:
                total_damage = sum([
                    random.randint(1, attack.dice_type) for _ in range(attack.roll_repetitions)
                ]) + attack.fixed_damage
                character.current_hp = character.current_hp - sum(total_damage)
                description += f"It deals {sum(total_damage)}"
            else:
                description += "It missed."
            action = EnemyActionDTO(
                action=CombatActionType.ATTACK,
                description=description,
                damage=total_damage,
                succeeded=attack_roll > character_armor_class,
            )
            actions.append(action)
        self.character_repository.update(character)
        return actions

    def player_action(self, quest_id: int, action: PlayerActionDTO) -> bool:
        encounter_record = self.encounter_repository.get_current_encounter_by_quest_id(quest_id)
        if not encounter_record:
            raise ValueError("No active encounter found for this quest.")
        
        character = self.character_repository.get_character_from_quest(quest_id)
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
        
        character = self.character_repository.get_character_from_quest(quest_id)
        target_enemy = self.enemy_repository.get(target_enemy_id)
        if not target_enemy:
            raise ValueError("Target enemy not found in the current encounter.")
        
        target_enemy.current_hp -= total_damage
        if target_enemy.current_hp <= 0:
            self.enemy_repository.delete_enemy(target_enemy.id)
        else:
            self.enemy_repository.update(target_enemy)
        enemy_records = self.enemy_repository.get_enemies_by_encounter_id(encounter_record.id)
        return [{"name": enemy.name, "id": enemy.id} for enemy in enemy_records]
 
