from app.database_sqlalchemy import SessionLocal
from app.models.user import User


def get_all_users():
    db = SessionLocal()

    try:
        users = db.query(User).all()

        return [
            {
                "id": user.id,
                "name": user.name,
                "role": user.role
            }
            for user in users
        ]
    finally:
        db.close()
