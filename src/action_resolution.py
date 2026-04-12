"""Resolve player combat actions (attack hit/miss, damage dice for frontend rolls)."""

from __future__ import annotations

import random
import re
from typing import Any

from .game import Game
from .narration import fetch_attack_miss_narration


def _dex_mod(dexterity: int) -> int:
    return (dexterity - 10) // 2


def enemy_armor_class(enemy) -> int:
    return 10 + _dex_mod(enemy.dexterity)


def parse_weapon_damage(damage: str) -> tuple[int, str | None, int]:
    """
    Parse a damage expression like '2d6+2', '1d12', '4d8 + 3'.
    Returns (dice_count, dice_type e.g. 'd6' or None, flat_bonus).
    """
    s = damage.strip().lower().replace(" ", "")
    m = re.match(r"^(\d+)d(\d+)([+-]\d+)?$", s)
    if m:
        n, sides = int(m.group(1)), int(m.group(2))
        bonus = int(m.group(3)) if m.group(3) else 0
        return n, f"d{sides}", bonus
    m2 = re.match(r"^(\d+)$", s)
    if m2:
        return 0, None, int(m2.group(1))
    return 1, "d6", 0


def _default_weapon_damage(game_data: dict[str, Any]) -> str:
    weapons = game_data.get("weapon") or []
    if weapons:
        return getattr(weapons[0], "damage", None) or "1d8"
    return "1d8"


def _enemy_index_from_target_id(target_id: str) -> int:
    m = re.match(r"^enemy_(\d+)$", target_id.strip())
    if not m:
        raise ValueError("target_id must look like 'enemy_0', 'enemy_1', …")
    return int(m.group(1))


def _resolve_enemy(game: Game, target_id: str):
    if not game.quests:
        raise ValueError("No active quest; call /start/ first.")
    quest = game.quests[-1]
    ei = game.current_encounter_index
    if ei < 0 or ei >= len(quest.encounters):
        raise ValueError("Invalid encounter state.")
    encounter = quest.encounters[ei]
    idx = _enemy_index_from_target_id(target_id)
    if idx < 0 or idx >= len(encounter.enemies):
        raise ValueError("No such foe in this encounter.")
    return encounter.enemies[idx]


# Placeholder until character creation supplies real attack bonus.
PLACEHOLDER_ATTACK_BONUS = 5


async def resolve_player_attack(game: Game, game_data: dict[str, Any], target_id: str) -> dict[str, Any]:
    enemy = _resolve_enemy(game, target_id)
    if enemy.hp <= 0:
        raise ValueError("That foe has already fallen.")

    ac = enemy_armor_class(enemy)
    d20 = random.randint(1, 20)
    total = d20 + PLACEHOLDER_ATTACK_BONUS
    hit = total >= ac

    if not hit:
        narr = await fetch_attack_miss_narration(
            target_name=enemy.species.name,
            attack_total=total,
            armor_class=ac,
            d20_roll=d20,
        )
        return {"success": False, "narration": narr}

    dmg_str = _default_weapon_damage(game_data)
    dice_count, dice_type, flat_bonus = parse_weapon_damage(dmg_str)

    payload: dict[str, Any] = {"success": True}
    if dice_count > 0 and dice_type:
        payload["rolls"] = dice_count
        payload["dice_type"] = dice_type
    else:
        payload["rolls"] = 0
        payload["dice_type"] = None
    if flat_bonus != 0:
        payload["flat_bonus"] = flat_bonus
    return payload
