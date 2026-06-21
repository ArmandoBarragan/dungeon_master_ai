from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from src.controllers.auth_controllers import router as auth_router
from src.controllers.game_controllers import router as game_router
from src.controllers.health_controllers import router as health_router
from config.db import init_db
from src.game_engine.game_loader import load_game

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    app.state.game_rules = load_game()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(game_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
