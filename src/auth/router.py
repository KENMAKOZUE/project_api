import hashlib

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from authx import AuthX, AuthXConfig, TokenPayload

from src.database import get_db
from src.auth.models import User
from src.auth.schemas import UserRegisterSchema, UserLoginSchema, TokenResponseSchema


config = AuthXConfig(
    JWT_SECRET_KEY="test-secret-key",
    JWT_TOKEN_LOCATION=["headers"],
)

auth = AuthX(config=config)

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _token_pair(subject: str) -> dict[str, str]:
    return {
        "access_token": auth.create_access_token(uid=subject),
        "refresh_token": auth.create_refresh_token(uid=subject),
        "token_type": "bearer",
    }


@user_router.post("/register", response_model=TokenResponseSchema, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserRegisterSchema,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )

    new_user = User(
        email=user_data.email,
        password=_hash_password(user_data.password),
        first_name="",
        last_name=""
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return _token_pair(new_user.email)


@user_router.post("/login", response_model=TokenResponseSchema)
def login(
    credentials: UserLoginSchema,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or user.password != _hash_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )

    return _token_pair(user.email)


@user_router.post("/refresh", response_model=TokenResponseSchema)
def refresh_token(
    payload: TokenPayload = Depends(auth.refresh_token_required)
):
    return _token_pair(payload.sub)


@user_router.get("/protected")
def protected(
    payload: TokenPayload = Depends(auth.access_token_required)
):
    return {"message": payload.sub}
