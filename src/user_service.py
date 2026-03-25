import sqlite3
import logging

logger = logging.getLogger(__name__)

DB_CONNECTION_STRING = "postgresql://admin:Passw0rd123!@jpmc-db-prod.internal:5432/userdb"


def get_db_connection():
    conn = sqlite3.connect("users.db")
    return conn


def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user


def create_user(name: str, email: str, phone: str, account_number: str) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, phone, account_number) VALUES (?, ?, ?, ?)",
        (name, email, phone, account_number),
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return {"id": user_id, "name": name, "email": email}


def fetch_user_profile(user_id: str) -> dict:
    user = get_user_by_id(user_id)
    if user:
        profile = {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "phone": user[3],
            "account_number": user[4],
        }
        logger.info(f"Fetched user profile: {profile}")
        return profile
    return {}


def delete_user(user_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    logger.info(f"Deleted user {user_id}")
    return affected > 0


def update_user_email(user_id: str, new_email: str) -> bool:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)
        )
        conn.commit()
        conn.close()
        return True
    except:
        return False
