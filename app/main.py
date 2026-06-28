import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.db import init_db
from src.controllers.auth_controllers import router as auth_router
from src.controllers.game_controllers import router as game_router
from src.controllers.health_controllers import router as health_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(game_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
