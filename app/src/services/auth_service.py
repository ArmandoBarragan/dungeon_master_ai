import hashlib
from datetime import UTC, datetime, timedelta

import bcrypt
from jose import jwt

from config.settings import JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET_KEY
from src.models import User
from src.repositories.user_repository import UserRepository


def _password_digest(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(_password_digest(password), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(_password_digest(password), hashed_password.encode())


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, name: str, email: str, password: str) -> tuple[User, str]:
        if self.user_repository.get_by_email(email):
            raise ValueError("Email already registered")

        hashed_password = hash_password(password)
        user = self.user_repository.create(name, email, hashed_password)
        return user, self._create_access_token(user.id)

    def login(self, email: str, password: str) -> tuple[User, str]:
        user = self.user_repository.get_by_email(email)
        if user is None or not verify_password(password, user.password):
            raise ValueError("Invalid email or password")

        return user, self._create_access_token(user.id)

    def _create_access_token(self, user_id: int) -> str:
        expires_at = datetime.now(UTC) + timedelta(minutes=JWT_EXPIRE_MINUTES)
        payload = {"sub": str(user_id), "exp": expires_at}
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    def get_user_id(self, token: str) -> int:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return int(payload["sub"])
        except jwt.JWTError:
            raise ValueError("Invalid token")