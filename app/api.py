from fastapi import FastAPI
from app.services.postgres_service import get_users

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to AI Career OS"}


@app.get("/users")
def users():
    users = get_users()

    return [
        {
            "id": user[0],
            "name": user[1],
            "role": user[2]
        }
        for user in users
    ]
from pydantic import BaseModel

class User(BaseModel):
    name: str
    role: str


@app.post("/users")
def create_user(user: User):
    from app.services.postgres_service import get_connection

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (name, role) VALUES (%s, %s)",
        (user.name, user.role)
    )

    conn.commit()

    cur.close()
    conn.close()

    return {"message": "User created successfully"}
