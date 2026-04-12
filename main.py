from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

from src import Game


load_dotenv()

app = FastAPI()

game = None


class ActionRequest(BaseModel):
    """Player choice from the encounter UI."""

    action: str = Field(default="attack", description="For now only 'attack' is supported.")
    target_id: str = Field(..., description="Foe id from /start/, e.g. enemy_0.")


@app.get("/start/")
async def start():
    global game
    game = Game.create_new()
    return JSONResponse(
        content={
            "initial_narration": game.quests[0].initial_narration,
            "incident_dialogue": game.quests[0].incident_dialogue,
        },
        status_code=200,
        headers={
            "Content-Type": "application/json",
        }
    )


@app.post("/action/")
async def action(body: ActionRequest):
    global game
    if game is None or not game.quests:
        raise HTTPException(status_code=400, detail="Start a game with GET /start/ first.")
    if body.action != "attack":
        raise HTTPException(status_code=400, detail="Only action='attack' is supported.")

    return JSONResponse(content={})


@app.post("/roll")
async def roll():
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
