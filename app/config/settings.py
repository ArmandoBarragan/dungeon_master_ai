import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") or os.environ.get("OpenAIKey")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = int(os.environ.get("APP_PORT", "8001"))

POSTGRES_USER = os.environ.get("POSTGRES_USER", "dungeon_master")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "dungeon_master_password")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "dungeon_master")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")

DATABASE_URL = os.environ.get("DATABASE_URL") or (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "change-me-in-production")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.environ.get("JWT_EXPIRE_MINUTES", "60"))
