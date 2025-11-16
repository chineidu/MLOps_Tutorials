from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


# ===
from pydantic import BaseModel


class User(BaseModel):
    username: str
    role: Role


# ===
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # Fake decode
    if token == "admin-token":
        return User(username="admin_user", role=Role.ADMIN)
    if token == "editor-token":
        return User(username="editor_user", role=Role.EDITOR)
    if token == "viewer-token":
        return User(username="viewer_user", role=Role.VIEWER)
    raise HTTPException(status_code=401, detail="Invalid token")


# ===
def role_required(required_roles: list[Role]):
    def wrapper(user: User = Depends(get_current_user)):
        if user.role not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Access denied for role: {user.role}")
        return user

    return wrapper


# ===
from fastapi import FastAPI
app = FastAPI()


@app.get("/admin/dashboard")
def admin_dashboard(user: User = Depends(role_required([Role.ADMIN]))):
    return {"message": f"Welcome to admin dashboard, {user.username}"}


@app.get("/editor/section")
def editor_section(user: User = Depends(role_required([Role.ADMIN, Role.EDITOR]))):
    return {"message": f"Welcome editor {user.username}"}
