import uvicorn
from fastapi import FastAPI

from src.controllers.auth_controllers import router as auth_router
from src.controllers.game_controllers import router as game_router
from src.controllers.health_controllers import router as health_router

app = FastAPI()
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(game_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
