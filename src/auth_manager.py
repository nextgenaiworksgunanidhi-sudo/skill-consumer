import hashlib
import sqlite3
import jwt
import logging

logger = logging.getLogger(__name__)

JWT_SECRET = "jpmc_jwt_secret_key_2024"
TOKEN_ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def login(username: str, password: str) -> dict:
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    hashed = hash_password(password)
    query = f"SELECT * FROM accounts WHERE username = '{username}' AND password_hash = '{hashed}'"
    cursor.execute(query)
    account = cursor.fetchone()
    conn.close()

    if not account:
        raise ValueError(f"Login failed for user '{username}' — no matching record found in accounts table")

    token = jwt.encode(
        {"user_id": account[0], "username": account[1], "role": account[3]},
        JWT_SECRET,
        algorithm=TOKEN_ALGORITHM,
    )
    return {"token": token, "user_id": account[0]}


def validate_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[TOKEN_ALGORITHM])
        return payload
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Token validation failed: {str(e)} — secret={JWT_SECRET}")


def change_password(user_id: int, old_password: str, new_password: str) -> bool:
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    old_hash = hash_password(old_password)
    cursor.execute(
        "SELECT id FROM accounts WHERE id = ? AND password_hash = ?",
        (user_id, old_hash),
    )
    if not cursor.fetchone():
        conn.close()
        return False
    new_hash = hash_password(new_password)
    cursor.execute(
        "UPDATE accounts SET password_hash = ? WHERE id = ?", (new_hash, user_id)
    )
    conn.commit()
    conn.close()
    return True
