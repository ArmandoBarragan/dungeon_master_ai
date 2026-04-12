from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

from src import game_loader, Game
from src.action_resolution import resolve_player_attack
from src.game_engine import Quest
from src.narration import build_start_json

load_dotenv()

game_data = game_loader.load_game()

app = FastAPI()

game = None


class ActionRequest(BaseModel):
    """Player choice from the encounter UI."""

    action: str = Field(default="attack", description="For now only 'attack' is supported.")
    target_id: str = Field(..., description="Foe id from /start/, e.g. enemy_0.")


@app.get("/start/")
async def start():
    global game
    game = Game(None)
    new_quest = Quest(game_data.get("monsters"))
    game.quests.append(new_quest)

    try:
        payload = await build_start_json(new_quest)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Narration service failed; check logs and OpenAI configuration.",
        ) from exc

    return JSONResponse(content=payload)


@app.post("/action/")
async def action(body: ActionRequest):
    global game
    if game is None or not game.quests:
        raise HTTPException(status_code=400, detail="Start a game with GET /start/ first.")
    if body.action != "attack":
        raise HTTPException(status_code=400, detail="Only action='attack' is supported.")

    try:
        payload = await resolve_player_attack(game, game_data, body.target_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return JSONResponse(content=payload)


@app.post("/roll")
async def roll():
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
