import sqlite3


DATABASE_NAME = "profiles.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            experience INTEGER NOT NULL,
            salary INTEGER NOT NULL,
            career_score INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_profile(name, role, experience, salary, career_score):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO profiles (name, role, experience, salary, career_score)
        VALUES (?, ?, ?, ?, ?)
    """, (name, role, experience, salary, career_score))

    connection.commit()
    connection.close()


def get_all_profiles():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, role, experience, salary, career_score
        FROM profiles
    """)

    profiles = cursor.fetchall()
    connection.close()

    return profiles


def update_profile(profile_id, name, role, experience, salary, career_score):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE profiles
        SET name = ?, role = ?, experience = ?, salary = ?, career_score = ?
        WHERE id = ?
    """, (name, role, experience, salary, career_score, profile_id))

    connection.commit()
    connection.close()


def delete_profile(profile_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM profiles
        WHERE id = ?
    """, (profile_id,))

    connection.commit()
    connection.close()