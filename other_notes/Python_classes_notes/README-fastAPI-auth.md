# FastAPI-Auth

## Table of Content

- [FastAPI-Auth](#fastapi-auth)
  - [Table of Content](#table-of-content)
  - [Sample File](#sample-file)

## Sample File

```py
# auth.py

from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Union

import uvicorn
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel
from rich.console import Console

console = Console()

auth_router = APIRouter(tags=["auth"])

# To get a string like this run:
# openssl rand -hex 32
SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer is used to get the token from the request headers.
# It sends the request to the tokenUrl endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


fake_users_db: dict[str, Any] = {
    "johndoe": {
        "user_id": 1,
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        # "password": "password",
        "hashed_password": "$2b$12$ZG6Xb2mFxt4jd.Fy6m6p..TyoiL5Q9e8vOPnB29SoRvO8IHeInxm2",
        "disabled": False,
    }
}


def get_db() -> dict[str, Any]:  # type: ignore
    try:
        yield fake_users_db
    finally:
        {}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None
    username: str | None = None


class User(BaseModel):
    user_id: int
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


db_dependency = Annotated[dict, Depends(get_db)]
auth_dependency = Annotated[str, Depends(oauth2_scheme)]


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(
    db: Session, username: str, password: str  # type: ignore
) -> Union[bool, Any]:
    """This returns the user if the user is correctly authenticated otherwise False."""
    user = get_user(db, username)
    if not user:
        return False
    verify_password = pwd_context.verify(password, user.hashed_password)
    if not verify_password:
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta) -> str:
    """This generates a string as an access token."""
    to_encode: dict[str, Any] = {"sub": username, "id": user_id}
    expire = datetime.now(timezone.utc) + expires_delta
    # Update the data with the expiration timedelta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency  # type: ignore
) -> dict[str, Any]:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        username=user.username,  # type: ignore
        user_id=user.user_id,  # type: ignore
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: auth_dependency) -> Union[HTTPException, Any]:
    """This authenticates and returns the current user by sending a request to
    `login_for_access_token`."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        username: str = payload.get("sub")

        if user_id is None or username is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, username=username)

    except JWTError:
        raise credentials_exception

    # TODO: Update this!
    user = get_user(fake_users_db, username=token_data.username) # type: ignore

    if user is None:
        raise credentials_exception
    return user


user_dependency = Annotated[dict[str, User], Depends(get_current_user)]


@auth_router.get("/users")
async def get_users(db: db_dependency, _: user_dependency) -> dict[str, User]: # type: ignore
    return db


```
