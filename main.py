from fastapi import FastAPI
from fastapi.responses import Response
from src import game_loader, Game
from src.game_engine import Quest
game_data = game_loader.load_game()

app = FastAPI()


@app.get("/start/")
async def start():
    # Generate character
    # Generate game
    # Game generates quest
    new_quest = Quest(game_data.get("monsters"))
    return Response(status_code=204)


@app.post("/action/")
async def action():
    # Get user response to event, respond with a new event
    return Response(status_code=204)


@app.post("/roll")
async def roll():
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
