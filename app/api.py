from fastapi import FastAPI
from pydantic import BaseModel

from app.database_sqlalchemy import SessionLocal
from app.models.user import User
from app.security import hash_password
from app.services.sqlalchemy_service import get_all_users

app = FastAPI()


class UserRequest(BaseModel):
    name: str
    role: str
    email: str
    password: str


@app.get("/")
def home():
    return {"message": "Welcome to AI Career OS"}


@app.get("/users")
def users():
    return get_all_users()


@app.post("/users")
def create_user(user: UserRequest):
    db = SessionLocal()

    try:
        existing_user = db.query(User).filter(User.email == user.email).first()

        if existing_user is not None:
            return {"message": "Email already registered"}

        new_user = User(
            name=user.name,
            role=user.role,
            email=user.email,
            password=hash_password(user.password)
        )

        db.add(new_user)
        db.commit()

        return {"message": "User created successfully"}

    finally:
        db.close()


@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserRequest):
    db = SessionLocal()

    try:
        existing_user = db.query(User).filter(User.id == user_id).first()

        if existing_user is None:
            return {"message": "User not found"}

        existing_user.name = user.name
        existing_user.role = user.role
        existing_user.email = user.email
        existing_user.password = hash_password(user.password)

        db.commit()

        return {"message": "User updated successfully"}

    finally:
        db.close()


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()

    try:
        existing_user = db.query(User).filter(User.id == user_id).first()

        if existing_user is None:
            return {"message": "User not found"}

        db.delete(existing_user)
        db.commit()

        return {"message": "User deleted successfully"}

    finally:
        db.close()
