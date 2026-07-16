import psycopg2


def get_connection():
    return psycopg2.connect(
        host="postgres",
        dbname="ai_career_os",
        user="stefano",
        password="password123"
    )


def get_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")

    users = cur.fetchall()

    cur.close()
    conn.close()

    return users
