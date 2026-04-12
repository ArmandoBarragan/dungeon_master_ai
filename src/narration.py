"""OpenAI-backed quest intro narrations and API payload helpers."""

from __future__ import annotations

import json
import os
from typing import Any

from openai import AsyncOpenAI

from .game_engine import Quest


def _openai_api_key() -> str | None:
    return os.getenv("OPENAI_API_KEY") or os.getenv("OpenAIKey")


def _enemy_attack_dicts(enemy) -> list[dict[str, Any]]:
    attacks = getattr(enemy.species, "attacks", None) or []
    out: list[dict[str, Any]] = []
    for a in attacks:
        if isinstance(a, dict):
            out.append({"name": a.get("name", ""), "damage": a.get("damage", "")})
        else:
            out.append({"name": getattr(a, "name", ""), "damage": getattr(a, "damage", "")})
    return out


def serialize_first_encounter_enemies(quest: Quest) -> list[dict[str, Any]]:
    """Stable ids for targeting; first encounter only."""
    if not quest.encounters:
        return []
    encounter = quest.encounters[0]
    rows: list[dict[str, Any]] = []
    for i, enemy in enumerate(encounter.enemies):
        species = enemy.species
        rows.append(
            {
                "id": f"enemy_{i}",
                "name": species.name,
                "hp": enemy.hp,
                "size": species.size,
                "attacks": _enemy_attack_dicts(enemy),
            }
        )
    return rows


def attack_options_from_enemies(enemies: list[dict[str, Any]]) -> list[dict[str, str]]:
    options: list[dict[str, str]] = []
    for row in enemies:
        eid = row["id"]
        name = row["name"]
        options.append(
            {
                "target_id": eid,
                "label": f"Attack the {name}",
            }
        )
    return options


def quest_brief_for_model(quest: Quest, enemies: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "location": quest.location,
        "reward_gold": quest.reward,
        "final_boss": quest.boss,
        "first_encounter_foes": [
            {
                "name": e["name"],
                "hp": e["hp"],
                "size": e["size"],
                "attacks": e["attacks"],
            }
            for e in enemies
        ],
    }


async def fetch_medieval_narrations(brief: dict[str, Any]) -> dict[str, str]:
    """Returns quest_narration and first_encounter_narration (medieval fantasy tone)."""
    api_key = _openai_api_key()
    if not api_key:
        raise RuntimeError("Missing API key: set OPENAI_API_KEY or OpenAIKey in the environment.")

    client = AsyncOpenAI(api_key=api_key)
    user_payload = json.dumps(brief, ensure_ascii=False)

    system = (
        "You are a medieval fantasy chronicler and dungeon master. "
        "Speak with a vivid, archaic-but-readable voice (thee/thou sparingly, rich imagery). "
        "You will receive structured quest facts including place names and monster names; "
        "keep those proper names exactly as given. "
        "Return ONLY a JSON object with two string fields: "
        '"quest_narration" (the quest hook: where they go, the promised reward, the shadow of the final foe) '
        'and "first_encounter_narration" (what the hero sees and feels as the first foes appear). '
        "If there are no foes listed, describe an eerie calm or foreshadowing instead of combat."
    )

    response = await client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_payload},
        ],
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    if not raw:
        raise RuntimeError("OpenAI returned an empty response.")

    data = json.loads(raw)
    quest_n = data.get("quest_narration", "")
    enc_n = data.get("first_encounter_narration", "")
    if not isinstance(quest_n, str) or not isinstance(enc_n, str):
        raise RuntimeError("OpenAI JSON missing expected string narrations.")

    return {"quest_narration": quest_n, "first_encounter_narration": enc_n}


async def fetch_attack_miss_narration(
    *,
    target_name: str,
    attack_total: int,
    armor_class: int,
    d20_roll: int,
) -> str:
    """Short medieval-flavored miss line; falls back if the API is unavailable."""
    api_key = _openai_api_key()
    brief = {
        "foe_name": target_name,
        "d20": d20_roll,
        "attack_total": attack_total,
        "armor_class": armor_class,
    }
    if not api_key:
        return (
            f"Thy strike goes wide: the blow totals {attack_total} against the "
            f"{target_name}'s guard (AC {armor_class}), and steel meets only shadow."
        )

    client = AsyncOpenAI(api_key=api_key)
    user_payload = json.dumps(brief, ensure_ascii=False)
    system = (
        "You are a medieval fantasy combat narrator. The hero's attack missed. "
        "Write ONE short paragraph (2–4 sentences), vivid archaic tone, proper name unchanged. "
        'Return ONLY JSON: {"narration": "<your text>"}'
    )
    try:
        response = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_payload},
            ],
            response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content
        if not raw:
            raise ValueError("empty")
        data = json.loads(raw)
        text = data.get("narration", "")
        if isinstance(text, str) and text.strip():
            return text.strip()
    except Exception:
        pass
    return (
        f"The {target_name} slips aside; thy tally of {attack_total} fails to pierce AC {armor_class}."
    )


async def build_start_json(quest: Quest) -> dict[str, Any]:
    enemies = serialize_first_encounter_enemies(quest)
    brief = quest_brief_for_model(quest, enemies)
    narr = await fetch_medieval_narrations(brief)

    return {
        "narrations": {
            "quest": narr["quest_narration"],
            "first_encounter": narr["first_encounter_narration"],
        },
        "enemies": enemies,
        "options": attack_options_from_enemies(enemies),
    }
